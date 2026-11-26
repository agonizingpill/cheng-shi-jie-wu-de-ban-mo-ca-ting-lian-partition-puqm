import json
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.queueing import broker, submit, result
from core.records import get, insert, need, scan, update
from domain.learning import calculate
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks

BAND_MIN = .05
BAND_MAX = .95
STALE_MESSAGE = '踏点或区线已更新，请重新分析'
TRIAL_STALE_MESSAGE = STALE_MESSAGE + '（试算已过期：同批补录踏点已经复核，须重新试算后再确认）'


def resolve_band(data):
    """从显式字段或额外别名中找到试调关注线。"""
    for name in ('control_band', 'trial_band', 'band', 'gauge', 'attention_line',
                 'trial_line', 'line', 'threshold', 'cutoff'):
        value = getattr(data, name, None)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    extra = getattr(data, 'model_extra', None) or {}
    for key, value in extra.items():
        if value is None:
            continue
        k = key.lower()
        if 'band' in k or 'gauge' in k or 'threshold' in k or 'cutoff' in k \
                or k == 'line' or k.endswith('_line'):
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


def verified_points(conn, panel_code, survey):
    panel = get(conn, studio_panels, panel_code)
    rows = [row for row in scan(conn, floor_readings) if row['panel'] == panel['code']
        and row['survey'] == survey and row['checked']]
    need(len(rows) >= 9, '已复核踏点不足 9 个')
    return panel, rows


def trial_payload(panel, survey, rows, band):
    trial = band is not None
    effective = float(band) if trial else float(panel['control_band'])
    if trial:
        need(BAND_MIN <= effective <= BAND_MAX, '演练关注线必须落在模拟量程')
    snapshot_panel = {**panel, 'control_band': effective}
    return {'panel': snapshot_panel, 'survey': survey, 'points': rows,
            'control_band': effective, 'trial': trial}


def store_ready(user, token, payload, results):
    """写入与 worker 完成态一致的计算凭证，供 /compute 与签认读取。"""
    broker.set(f'compute:{token}', json.dumps(
        {'owner': user['sub'], 'status': 'ready', 'input': payload, 'result': results},
        allow_nan=False), ex=86400)


def cluster_floor(conn, user, data):
    panel, rows = verified_points(conn, data.panel, data.survey)
    band = resolve_band(data)
    payload = trial_payload(panel, data.survey, rows, band)
    job = submit(user, payload)
    return {**job, 'control_band': payload['control_band'], 'trial': payload['trial']}


def trial_floor_now(conn, user, data):
    """试调关注线的同步试算：立即返回分组结果，同时留存可确认的凭证。"""
    panel, rows = verified_points(conn, data.panel, data.survey)
    band = resolve_band(data)
    payload = trial_payload(panel, data.survey, rows, band)
    results = calculate(payload)
    token = uuid4().hex
    store_ready(user, token, payload, results)
    return {'token': token, 'status': 'ready', 'control_band': payload['control_band'],
            'trial': True, **results}


def _survey_by_token(conn, token):
    row = conn.execute(select(optics_surveys).where(optics_surveys.c.token == token)).mappings().first()
    return dict(row) if row is not None else None


def _survey_by_code(conn, code):
    row = conn.execute(select(optics_surveys).where(optics_surveys.c.code == code)).mappings().first()
    return dict(row) if row is not None else None


def _resolve_run(conn, user, data):
    """返回 (snapshot, results, token)。无 token 时支持按 panel/survey 直接确认。"""
    token = getattr(data, 'token', None)
    if token:
        run = result(user, token)
        return run['input'], run['result'], token
    panel_code = getattr(data, 'panel', None)
    survey = getattr(data, 'survey', None)
    need(bool(panel_code and survey), '须提供试算凭证或分区与走测轮次')
    panel, rows = verified_points(conn, panel_code, survey)
    band = resolve_band(data)
    payload = trial_payload(panel, survey, rows, band)
    results = calculate(payload)
    token = uuid4().hex
    store_ready(user, token, payload, results)
    return payload, results, token


def sign_scan(conn, user, data):
    requested_band = resolve_band(data)
    request_token = getattr(data, 'token', None)
    had_token = bool(request_token)

    # 凭分析凭证的幂等重试：同一试算已签认则直接返回既有记录。
    if request_token:
        existing = _survey_by_token(conn, request_token)
        if existing is not None:
            return existing

    # 凭分析簿编号的幂等重试（含无 token 的直接确认）。
    code = getattr(data, 'code', None)
    if code:
        same_code = _survey_by_code(conn, code)
        if same_code is not None:
            need(not request_token or same_code['token'] == request_token,
                 '分析簿编号已被其他试算占用，请更换编号')
            return same_code

    snapshot, results, token = _resolve_run(conn, user, data)
    panel = get(conn, studio_panels, snapshot['panel']['code'], lock=True)

    active = [p for p in scan(conn, floor_readings) if p['checked'] and p['panel'] == panel['code']
        and p['survey'] == snapshot['survey']]
    trial = bool(snapshot.get('trial'))
    if had_token and not trial and requested_band is None:
        # 兼容既有分析流程：关注线或踏点快照变化都要求重新分析。
        need(panel == snapshot['panel'] and active == snapshot['points'], STALE_MESSAGE)
    else:
        # 试算/直接确认：关注线待本次切换，只以同批已复核踏点是否补录复核判过期。
        need(active == snapshot['points'], TRIAL_STALE_MESSAGE)

    # 签认时若另行指定关注线，按该线对同一批点重算，保证簿内分组与签认线一致。
    band = float(snapshot.get('control_band', snapshot['panel']['control_band']))
    if requested_band is not None and abs(requested_band - band) > 1e-12:
        need(BAND_MIN <= requested_band <= BAND_MAX, '演练关注线必须落在模拟量程')
        band = requested_band
        results = calculate({'panel': {**snapshot['panel'], 'control_band': band},
                             'points': snapshot['points']})

    code = code or f"SCAN-{uuid4().hex[:24]}"
    values = dict(code=code, panel=panel['code'], survey=snapshot['survey'], token=token,
                  control_band=band,
                  **{k: results[k] for k in ('low_points', 'members', 'clusters', 'noise')})
    try:
        # 保存点冲突时回滚到保存点，兼容并发/重复确认。
        with conn.begin_nested():
            conn.execute(optics_surveys.insert().values(**values))
    except IntegrityError:
        replay = _survey_by_token(conn, token) or _survey_by_code(conn, code)
        if replay is not None:
            return replay
        raise

    # 关注线与签认分析在同一事务内一次性切换；任一步失败整体回滚。
    conn.execute(studio_panels.update().where(studio_panels.c.code == panel['code']).values(
        control_band=band, active_review=code))
    return get(conn, optics_surveys, code)
