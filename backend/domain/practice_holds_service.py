from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks


def post_hold(conn, user, data):
    scan_row = get(conn,optics_surveys,data.review)
    panel = get(conn,studio_panels,scan_row['panel'],lock=True)
    point = get(conn,floor_readings,data.point)
    need(data.shift.startswith(('AM-','EV-')),'须填写有效课程时段编号')
    need(point['panel']==panel['code'] and point['code'] in scan_row['low_points']
        and point['slide']<panel['control_band'],'该踏点不在签认的独立点位中')
    base = [row for row in scan(conn,dance_blocks) if row['live_panel']==panel['code']
        and row['shift']==data.shift and row['state']=='已开课']
    need(not base,'该区有已开课班级，需先由场地主任终止现场课程')
    return insert(conn,practice_holds,**data.model_dump(),panel=panel['code'],
        scope_key=f"{panel['code']}:{data.shift}",status='停练',retest=None)


def clear_hold(conn, user, data):
    item = get(conn,practice_holds,data.hold)
    panel = get(conn,studio_panels,item['panel'],lock=True)
    item = get(conn,practice_holds,data.hold,lock=True)
    original, follow = (get(conn,floor_readings,key) for key in (item['point'],data.retest))
    need(item['status']=='停练','该围挡已经解除')
    need(follow['checked'] and follow['panel']==panel['code'] and follow['survey']!=original['survey']
        and (follow['x_cm'],follow['y_cm'])==(original['x_cm'],original['y_cm'])
        and follow['slide']>=panel['control_band'],'须提交下轮同位置已复核的恢复读数')
    return update(conn,practice_holds,data.hold,status='已解封',retest=follow['code'],scope_key=None)
