from sqlalchemy import select


def contains(panel, x, y):
    return panel["x1"] <= x < panel["x2"] and panel["y1"] <= y < panel["y2"]


def blocked(conn, holds, panel, shift):
    query = select(holds.c.code).where(holds.c.panel == panel, holds.c.shift == shift, holds.c.status == "停练")
    return conn.execute(query).first() is not None
