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
    need(.05 <= data.control_band <= .95, '演练关注线必须落在模拟量程')
    return update(conn, studio_panels, panel['code'], control_band=data.control_band)
