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
            contact_name TEXT,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')


    con.commit()

def wipe_db(con: sqlite3.Connection):
    verification = input("This will wipe all data from the database. Type 'YES' to confirm: ").strip()

    if verification != "YES":
        print("Wipe cancelled--no data was lost.")
        return False
    
    else:
        con.executescript("""
        DELETE FROM lab_x_topics;
        DELETE FROM contacts;
        DELETE FROM topics;
        DELETE FROM labs;
                          """)
        con.commit()
        print("Wipe completed--all data was wiped.")
        return True
    

def migrate(con: sqlite3.Connection, csv_path=CSV_PATH):
    """Reads CSV file and inserts data into the database"""
    cursor = con.cursor()
    df = pd.read_csv(csv_path)
    inserted = 0 # keeps track of count of inserted data vals

    # Checking what's been in memory instead of constantly verifying each row.
    existing_titles = {row["title"] for row in con.execute("SELECT title FROM labs")}
    topic_ids = {row["name"]: row["id"] for row in con.execute("SELECT name, id FROM topics")}

    # Read row data from CSV, insert it into the database
    for _, row in df.iterrows():

        # to 'labs'
        title = row["Title"]
        if title in existing_titles:  # checks the data is not already in db
            continue

        if pd.notna(row["Website"]):
            website = row["Website"]
        else:
            website = None
        
        if pd.notna(row["Recruiting Status"]):
            status = row["Recruiting Status"]
        else:
            status = "Unknown"

        con.execute("INSERT INTO labs (title, website, recruiting_status) VALUES (?, ?, ?)",(title, website, status))
        lab_id = cursor.lastrowid # for lab_x_topics

        # to 'topics'
        for topic_name in row["Topics"].split(","):
            topic_name = topic_name.strip()
            if topic_name not in topic_ids:
                con.execute("INSERT INTO topics (name) VALUES (?)", (topic_name,))
                topic_ids[topic_name] = cursor.lastrowid # for lab_x_topics

            # to 'lab_x_topics'
            con.execute("INSERT INTO lab_x_topics (lab_id, topic_id) VALUES (?, ?)", (lab_id, topic_ids[topic_name]))
            inserted = inserted + 1

        
    con.commit()
    return inserted

if __name__ == "__main__":
    con = get_connection()
    try:
        setup_db(con)
    finally:
        con.close()