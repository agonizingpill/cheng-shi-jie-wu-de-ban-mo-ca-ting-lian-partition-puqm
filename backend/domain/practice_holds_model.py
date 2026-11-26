from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


practice_holds = Table('practice_holds', metadata,
    Column('code', String(64), primary_key=True),
    Column('panel', String(160), ForeignKey('studio_panels.code'), nullable=False),
    Column('point', String(160), ForeignKey('floor_readings.code'), nullable=False),
    Column('review', String(160), ForeignKey('optics_surveys.code'), nullable=False),
    Column('shift', String(160), nullable=False),
    Column('scope_key', String(160), nullable=True, unique=True),
    Column('reason', String(160), nullable=False),
    Column('status', String(160), nullable=False),
    Column('retest', String(160), ForeignKey('floor_readings.code'), nullable=True),
    CheckConstraint("status IN ('停练','已解封')"),
)
