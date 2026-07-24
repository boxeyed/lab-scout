import pandas as pd
import sqlite3

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 
def setup_db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
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
            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS contacts (
            lab_id INTEGER PRIMARY KEY,
            email TEXT,
            contact_name TEXT,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')


    con.commit()
    con.close()

def wipe_db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
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
        con.close()

        print("Wipe completed--all data was wiped.")
        return True
    

def migrate():
    """Reads CSV file and inserts data into the database"""
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")

    df = pd.read_csv(CSV_PATH)
    inserted = 0 # keeps track of count of inserted data vals

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

        lab_id = con.execute("INSERT INTO labs (title, website, recruiting_status) VALUES (?, ?, ?)",(title, website, status))
        lab_id = lab_id.lastrowid # for lab_x_topics

        # to 'topics'
        for topic_name in row["Topics"].split(","):
            topic_name = topic_name.strip()
            if topic_name not in topic_ids:
                cursor = con.execute("INSERT INTO topics (name) VALUES (?)", (topic_name,)) # the internal cursor return
                topic_ids[topic_name] = cursor.lastrowid # for lab_x_topics

            # to 'lab_x_topics'
            con.execute("INSERT INTO lab_x_topics (lab_id, topic_id) VALUES (?, ?)", (lab_id, topic_ids[topic_name]))
            inserted = inserted + 1

        # to 'contacts
        if pd.notna(row["Contact Name"]):
            name = row["Contact Name"]
        
        if pd.notna(row["Contact Email"]):
            email = row["Contact Email"]

        

        
    con.commit()
    con.close()

    print("Migration completed--database updated.")
    return inserted

def ask_migrate_or_clear():
        check = input("Choose from the following options:\n1. Migrate csv file to database\n2. Clear database\n-> ")

        if check!='1' and check!='2':
            print("Invalid input. Try again.")
            return -1
        elif check=='1':
            migrate()
        else:
            wipe_db()

if __name__ == "__main__":
    setup_db()
    ask_migrate_or_clear()