from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import practice_holds_service as service
from domain.practice_holds_model import practice_holds
from domain.practice_holds_schemas import PostHold, ClearHold

router = APIRouter()

@router.get('/practice_holds')
def list_practice_holds(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, practice_holds)


@router.post('/practice_holds/post-hold')
def post_hold(data: PostHold, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.post_hold(conn, user, data)
        record(conn, user, 'practice_holds.post_hold')
        return output


@router.post('/practice_holds/clear-hold')
def clear_hold(data: ClearHold, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.clear_hold(conn, user, data)
        record(conn, user, 'practice_holds.clear_hold')
        return output
