
from .db import get_conn

def insert_incident(incident_id, category, severity, description, detected_date, resolved_date=None):
    conn = get_conn()
    conn.execute("""
    INSERT INTO t_incidents (incident_id, category, severity, description, detected_date, resolved_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (incident_id, category, severity, description, detected_date, resolved_date))
    conn.commit()
    conn.close()

def get_incident(incident_id):
    conn = get_conn()
    cur = conn.execute("SELECT * FROM t_incidents WHERE incident_id = ?", (incident_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def list_incidents():
    conn = get_conn()
    cur = conn.execute("SELECT * FROM t_incidents ORDER BY detected_date DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]