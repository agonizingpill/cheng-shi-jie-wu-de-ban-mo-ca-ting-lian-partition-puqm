from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks


def set_gauge(conn, user, data):
    panel = get(conn, studio_panels, data.panel, lock=True)
    band = data.resolved_band() if hasattr(data, 'resolved_band') else data.control_band
    need(band is not None, '须提供演练关注线 control_band')
    need(.05 <= band <= .95, '演练关注线必须落在模拟量程')
    return update(conn, studio_panels, panel['code'], control_band=band)


def preview_gauge(conn, user, data):
    """试调关注线：只返回叠加候选线的分区视图，不写库、不影响排课。"""
    panel = get(conn, studio_panels, data.panel)
    band = data.resolved_band() if hasattr(data, 'resolved_band') else data.control_band
    need(band is not None, '须提供试调关注线 control_band')
    need(.05 <= band <= .95, '演练关注线必须落在模拟量程')
    return {**panel, 'control_band': band, 'trial': True, 'persisted_band': panel['control_band']}
