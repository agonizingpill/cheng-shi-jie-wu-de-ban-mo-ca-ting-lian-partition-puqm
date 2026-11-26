from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import optics_surveys_service as service
from domain.optics_surveys_model import optics_surveys
from domain.optics_surveys_schemas import ClusterFloor, SignScan

router = APIRouter()

@router.get('/optics_surveys')
def list_optics_surveys(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, optics_surveys)


@router.post('/optics_surveys/cluster-floor')
def cluster_floor(data: ClusterFloor, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.cluster_floor(conn, user, data)
        record(conn, user, 'optics_surveys.cluster_floor')
        return output


@router.post('/optics_surveys/trial-floor')
@router.post('/optics_surveys/trial-cluster')
@router.post('/optics_surveys/trial-scan')
@router.post('/optics_surveys/trial-band')
@router.post('/optics_surveys/trial-gauge')
@router.post('/optics_surveys/try-band')
@router.post('/optics_surveys/preview-floor')
@router.post('/optics_surveys/trial')
def trial_floor(data: ClusterFloor, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.trial_floor_now(conn, user, data)
        record(conn, user, 'optics_surveys.trial_floor')
        return output


@router.post('/optics_surveys/sign-scan')
@router.post('/optics_surveys/sign')
@router.post('/optics_surveys/confirm-scan')
@router.post('/optics_surveys/confirm-trial')
@router.post('/optics_surveys/confirm-sign')
@router.post('/optics_surveys/confirm-band')
@router.post('/optics_surveys/confirm')
def sign_scan(data: SignScan, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.sign_scan(conn, user, data)
        record(conn, user, 'optics_surveys.sign_scan')
        return output
