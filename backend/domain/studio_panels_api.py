from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import studio_panels_service as service
from domain.studio_panels_model import studio_panels
from domain.studio_panels_schemas import SetGauge

router = APIRouter()

@router.get('/studio_panels')
def list_studio_panels(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, studio_panels)


@router.post('/studio_panels/set-gauge')
def set_gauge(data: SetGauge, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.set_gauge(conn, user, data)
        record(conn, user, 'studio_panels.set_gauge')
        return output
