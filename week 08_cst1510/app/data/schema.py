def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """
    
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print(" Users table created successfully!")

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        date TEXT
    );
    """
    
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print(" Cyber incidents table created!")

def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        source TEXT,
        category TEXT,
        size INTEGER
    );
    """
    
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print(" Datasets metadata table created!")

def create_it_tickets_table(conn):
    """
    Create the it_tickets table with columns expected by app/data/tickets.py
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        ticket_id TEXT PRIMARY KEY,
        title TEXT,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        category TEXT,
        subject TEXT,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT
    );
    """
    
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print(" IT tickets table created!")


def create_all_tables(conn):
    """
    Create all tables for the intelligence platform.
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)