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

def search_inj_db(conn, inj_number):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM injectors WHERE injector_number = ? OR alt_inj_number_1 = ? OR alt_inj_number_2 = ?
    ''', (inj_number, inj_number, inj_number))

    result = cursor.fetchone()
    if result:
        return {
            "inj_number": result[0],
            "alt_inj_number_1": result[1],
            "alt_inj_number_2": result[2],
            "engine": result[3],
            "ms_2_5": result[4],
            "ms_1_0": result[5],
            "ms_1_5": result[6]
        }
    else:
        return None


def close_db(conn):
    conn.commit()
    conn.close()
