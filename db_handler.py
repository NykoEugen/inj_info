import sqlite3


def connect_db():
    conn = sqlite3.connect('injectors.db')
    return conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS injectors (
            injector_number TEXT PRIMARY KEY,
            alt_inj_number_1 TEXT,
            alt_inj_number_2 TEXT,
            engine TEXT,
            ms_2_5 INTEGER NOT NULL,
            ms_1_0 INTEGER NOT NULL,
            ms_1_5 INTEGER NOT NULL
        )
        ''')
    conn.commit()


def close_db(conn):
    conn.commit()
    conn.close()
