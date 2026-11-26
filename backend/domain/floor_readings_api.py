from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import floor_readings_service as service
from domain.floor_readings_model import floor_readings
from domain.floor_readings_schemas import RecordStep, VerifyStep

router = APIRouter()

@router.get('/floor_readings')
def list_floor_readings(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, floor_readings)


@router.post('/floor_readings/record-step')
def record_step(data: RecordStep, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.record_step(conn, user, data)
        record(conn, user, 'floor_readings.record_step')
        return output


@router.post('/floor_readings/verify-step')
def verify_step(data: VerifyStep, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.verify_step(conn, user, data)
        record(conn, user, 'floor_readings.verify_step')
        return output
