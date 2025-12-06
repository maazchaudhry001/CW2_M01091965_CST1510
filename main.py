# main.py (project root)
from app.data.schema import create_all_tables
from app.data.tickets import insert_ticket, list_tickets
from app.data.users import insert_user
from app.services.user_service import authenticate
from app.data.db import connect_database   # important!

def main():
    print("Initializing database...")
    conn = connect_database()
    try:
        # create tables using the open connection
        create_all_tables(conn)

        # demo/test data
        insert_user("admin67892341239987", "admin123", "admin")
        insert_ticket("TCK001122", "Test Title", "High", "Open", "Software",
                      "Login Issue", "2024-09-12","2024-09-16","test")

        print("Tickets:")
        print(list_tickets())

        print("Auth Test:", authenticate("admin", "admin123"))

    finally:
        conn.close()

if __name__ == "__main__":
    main()
