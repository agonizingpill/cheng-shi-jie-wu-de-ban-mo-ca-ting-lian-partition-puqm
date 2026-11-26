from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.studio_panels_model import studio_panels
from domain.floor_readings_model import floor_readings
from domain.optics_surveys_model import optics_surveys
from domain.practice_holds_model import practice_holds
from domain.dance_blocks_model import dance_blocks


def move_class(conn, user, data):
    from domain.floorplan import blocked
    course = get(conn,dance_blocks,data.course)
    codes = sorted(set((course['live_panel'],data.to_panel)))
    panels = {code:get(conn,studio_panels,code,lock=True) for code in codes}
    current = get(conn,dance_blocks,data.course,lock=True)
    need(course['live_panel']==current['live_panel'],'课程分区已变更，请刷新')
    source,target = panels[current['live_panel']],panels[data.to_panel]
    need(current['state']!='已开课' and source['code']!=target['code'],'该课不可改至当前分区')
    need(source['room']==target['room'],'仅可在当前舞室内改派')
    need(blocked(conn,practice_holds,source['code'],current['shift']),'当前区域未停练，保留原排课')
    need(not blocked(conn,practice_holds,target['code'],current['shift']),'目标分区也受围挡限制')
    used = sum(row['headcount'] for row in scan(conn,dance_blocks) if row['code']!=current['code']
        and row['live_panel']==target['code'] and row['shift']==current['shift'])
    need(used+current['headcount']<=target['people'],'目标分区当班人数超额')
    return update(conn,dance_blocks,data.course,live_panel=target['code'],move_note=data.reason,state='已调区')


def open_class(conn, user, data):
    from domain.floorplan import blocked
    course = get(conn,dance_blocks,data.course)
    panel = get(conn,studio_panels,course['live_panel'],lock=True)
    current = get(conn,dance_blocks,data.course,lock=True)
    need(course['live_panel']==current['live_panel'] and current['state']!='已开课','课程状态已改变')
    need(not blocked(conn,practice_holds,panel['code'],current['shift']),'该课程当前分区停练，请先调区')
    return update(conn,dance_blocks,data.course,state='已开课')
