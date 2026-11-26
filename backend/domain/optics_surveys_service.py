from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks


def cluster_floor(conn, user, data):
    panel = get(conn,studio_panels,data.panel)
    rows = [row for row in scan(conn,floor_readings) if row['panel']==panel['code']
        and row['survey']==data.survey and row['checked']]
    need(len(rows) >= 9,'已复核踏点不足 9 个')
    return submit(user,{'panel':panel,'survey':data.survey,'points':rows})


def sign_scan(conn, user, data):
    run = result(user,data.token)
    snapshot, results = run['input'], run['result']
    panel = get(conn,studio_panels,snapshot['panel']['code'],lock=True)
    active = [p for p in scan(conn,floor_readings) if p['checked'] and p['panel']==panel['code']
        and p['survey']==snapshot['survey']]
    need(panel==snapshot['panel'] and active==snapshot['points'],'踏点或区线已更新，请重新分析')
    return insert(conn,optics_surveys,code=data.code,panel=panel['code'],survey=snapshot['survey'],
        token=data.token,**{k:results[k] for k in ('low_points','members','clusters','noise')})
