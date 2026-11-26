from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


floor_readings = Table('floor_readings', metadata,
    Column('code', String(64), primary_key=True),
    Column('panel', String(160), ForeignKey('studio_panels.code'), nullable=False),
    Column('survey', String(160), nullable=False),
    Column('x_cm', Integer, nullable=False),
    Column('y_cm', Integer, nullable=False),
    Column('slide', Float, nullable=False),
    Column('capture_key', String(160), nullable=False, unique=True),
    Column('checked', Boolean, nullable=False),
    CheckConstraint('slide BETWEEN 0 AND 1'),
    CheckConstraint('x_cm >= 0'),
    CheckConstraint('y_cm >= 0'),
)
