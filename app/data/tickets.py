
from .db import connect_database
from datetime import datetime

def insert_ticket(ticket_id, priority, status, category, subject,
                  description=None, created_date=None,
                  resolved_date=None, assigned_to=None):
    
    if created_date is None:
        created_date = datetime.now().strftime("%Y-%m-%d")

    conn = connect_database()
    conn.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, 
         created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject,
          description, created_date, resolved_date, assigned_to))
    
    conn.commit()
    conn.close()


def get_ticket(ticket_id):
    conn = connect_database()
    cur = conn.execute("SELECT * FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def list_tickets(limit=100, offset=0):
    conn = connect_database()
    cur = conn.execute("""
        SELECT * FROM it_tickets 
        ORDER BY created_date DESC 
        LIMIT ? OFFSET ?
    """, (limit, offset))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]



def get_open_tickets():
    conn = connect_database()
    cur = conn.execute("""
        SELECT * FROM it_tickets
        WHERE status IN ('Open', 'In Progress')
        ORDER BY created_date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def resolve_ticket(ticket_id, resolved_date=None, new_status="Resolved"):
    if resolved_date is None:
        resolved_date = datetime.now().strftime("%Y-%m-%d")

    conn = connect_database()
    cur = conn.execute("""
        UPDATE it_tickets
        SET status = ?, resolved_date = ?
        WHERE ticket_id = ?
    """, (new_status, resolved_date, ticket_id))
    conn.commit()
    conn.close()
    return cur.rowcount > 0