import sqlite3


def connect_db():
    conn = sqlite3.connect('injectors.db')
    return conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS injectors (
            injector_number TEXT PRIMARY KEY,
            engine TEXT,
            2.5ms INTEGER NOT NULL,
            1.0ms INTEGER NOT NULL,
            1.5ms INTEGER NOT NULL
        )
        ''')
    conn.commit()


def close_db(conn):
    conn.commit()
    conn.close()
