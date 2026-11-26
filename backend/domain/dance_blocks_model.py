from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


dance_blocks = Table('dance_blocks', metadata,
    Column('code', String(64), primary_key=True),
    Column('course', String(160), nullable=False),
    Column('shift', String(160), nullable=False),
    Column('headcount', Integer, nullable=False),
    Column('home_panel', String(160), ForeignKey('studio_panels.code'), nullable=False),
    Column('live_panel', String(160), ForeignKey('studio_panels.code'), nullable=False),
    Column('move_note', String(160), nullable=True),
    Column('state', String(160), nullable=False),
    CheckConstraint('headcount BETWEEN 1 AND 40'),
    CheckConstraint("state IN ('已排','已调区','已开课')"),
)
