from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import dance_blocks_service as service
from domain.dance_blocks_model import dance_blocks
from domain.dance_blocks_schemas import MoveClass, OpenClass

router = APIRouter()

@router.get('/dance_blocks')
def list_dance_blocks(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, dance_blocks)


@router.post('/dance_blocks/move-class')
def move_class(data: MoveClass, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.move_class(conn, user, data)
        record(conn, user, 'dance_blocks.move_class')
        return output


@router.post('/dance_blocks/open-class')
def open_class(data: OpenClass, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.open_class(conn, user, data)
        record(conn, user, 'dance_blocks.open_class')
        return output
