from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks


def record_step(conn, user, data):
    from domain.floorplan import contains
    panel = get(conn,studio_panels,data.panel,lock=True)
    need(contains(panel,data.x_cm,data.y_cm),'踏点超出胶带分区')
    need(0<=data.slide<=1 and data.survey.startswith('SUR-'), '测值或走测批号有误')
    key = f"{data.survey}:{data.panel}:{data.x_cm}:{data.y_cm}"
    return insert(conn, floor_readings, **data.model_dump(), capture_key=key,checked=False)


def verify_step(conn, user, data):
    point = get(conn,floor_readings,data.point)
    get(conn,studio_panels,point['panel'],lock=True)
    point = get(conn,floor_readings,data.point,lock=True)
    need(not point['checked'],'踏点已经复核')
    return update(conn,floor_readings,data.point,checked=True)
