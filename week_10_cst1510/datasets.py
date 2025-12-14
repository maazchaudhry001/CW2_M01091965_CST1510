
from .db import get_conn

def insert_dataset(name, source, record_count, imported_date):
    conn = get_conn()
    conn.execute("""
    INSERT INTO t_datasets (dataset_name, source, record_count, imported_date)
    VALUES (?, ?, ?, ?)
    """, (name, source, record_count, imported_date))
    conn.commit()
    conn.close()

def list_datasets():
    conn = get_conn()
    cur = conn.execute("SELECT * FROM t_datasets ORDER BY imported_date DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
