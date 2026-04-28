import sqlite3

DB_FILE = 'hospital_management.db'

def run_query(query, params=(), fetch=False):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()

def create_tables():
    run_query("CREATE TABLE IF NOT EXISTS Admin (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    run_query("CREATE TABLE IF NOT EXISTS Doctor (id INTEGER PRIMARY KEY, name TEXT, username TEXT UNIQUE, password TEXT, status TEXT DEFAULT 'available')")
    run_query("CREATE TABLE IF NOT EXISTS Patient (id INTEGER PRIMARY KEY, name TEXT, username TEXT UNIQUE, password TEXT)")
    
    run_query("CREATE TABLE IF NOT EXISTS Appointment (id INTEGER PRIMARY KEY, p_id INTEGER, d_id INTEGER, date TEXT, time TEXT, FOREIGN KEY(p_id) REFERENCES Patient(id), FOREIGN KEY(d_id) REFERENCES Doctor(id))")
    run_query("CREATE TABLE IF NOT EXISTS Prescription (id INTEGER PRIMARY KEY, d_id INTEGER, p_id INTEGER, meds TEXT)")
    
    run_query("INSERT OR IGNORE INTO Admin (username, password) VALUES ('admin', 'admin123')")