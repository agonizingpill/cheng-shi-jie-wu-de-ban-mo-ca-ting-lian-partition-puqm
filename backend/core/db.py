from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine, inspect, text

from core.config import DATABASE_URL

metadata = MetaData()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@contextmanager
def transaction():
    with engine.begin() as conn:
        yield conn


def ensure_columns():
    """metadata.create_all 只建表不补列；为旧数据卷补齐本迭代新增的可空列。"""
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    with engine.begin() as conn:
        for table in metadata.sorted_tables:
            if table.name not in existing:
                continue
            present = {column['name'] for column in inspect(conn).get_columns(table.name)}
            for column in table.columns:
                if column.name in present:
                    continue
                column_type = column.type.compile(engine.dialect)
                conn.execute(text(
                    f'ALTER TABLE {table.name} ADD COLUMN {column.name} {column_type}'))
