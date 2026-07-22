import pandas as pd
import sqlite3

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 

def get_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def setup_db(con: sqlite3.Connection):
    cursor = con.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS labs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            website TEXT,
            recruiting_status TEXT DEFAULT "Unknown"
        );
        
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS lab_x_topics (
            lab_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            PRIMARY KEY (lab_id, topic_id),
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE, 
            FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS contacts (
            lab_id INTEGER PRIMARY KEY,
            email TEXT,
            researcher TEXT,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')


    con.commit()
    con.close()

def wipe_db(con: sqlite3.Connection):
    verification = input("This will wipe all data from the database. Type 'YES' to confirm: ").strip

    if verification != "YES":
        print("Wipe cancelled--no data was lost.")
        return False
    
    else:
        con.executescript("""
        DELETE FROM lab_topics;
        DELETE FROM contacts;
        DELETE FROM topics;
        DELETE FROM labs;
                          """)
        con.commit()
        print("Wipe completed--all data was wiped.")
        return True
    

if __name__ == "__main__":
    con = get_connection()
    try:
        setup_db(con)
    finally:
        con.close()