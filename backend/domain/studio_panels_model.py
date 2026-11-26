from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


studio_panels = Table('studio_panels', metadata,
    Column('code', String(64), primary_key=True),
    Column('room', String(160), nullable=False),
    Column('label', String(160), nullable=False),
    Column('x1', Integer, nullable=False),
    Column('y1', Integer, nullable=False),
    Column('x2', Integer, nullable=False),
    Column('y2', Integer, nullable=False),
    Column('people', Integer, nullable=False),
    Column('control_band', Float, nullable=False),
    CheckConstraint('x2 > x1'),
    CheckConstraint('y2 > y1'),
    CheckConstraint('people BETWEEN 1 AND 40'),
    CheckConstraint('control_band BETWEEN 0 AND 1'),
)
