from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


optics_surveys = Table('optics_surveys', metadata,
    Column('code', String(64), primary_key=True),
    Column('panel', String(160), ForeignKey('studio_panels.code'), nullable=False),
    Column('survey', String(160), nullable=False),
    Column('low_points', JSON, nullable=False),
    Column('members', JSON, nullable=False),
    Column('clusters', Integer, nullable=False),
    Column('noise', Integer, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
    CheckConstraint('clusters >= 0'),
    CheckConstraint('noise >= 0'),
)
