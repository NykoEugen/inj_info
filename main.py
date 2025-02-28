from db_handler import connect_db, create_table, close_db
from gui import run_gui


def main():
    conn = connect_db()
    create_table(conn)
    run_gui(conn)
    close_db(conn)


if __name__ == "__main__":
    main()
