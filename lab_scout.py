import pandas as pd
import sqlite3
from manage_db import setup_db, ask_migrate_or_clear, get_con
from input_getter import scout_lab_input, add_lab_input

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 
def scout_labs(connection: sqlite3.Connection):
    """Ask the user for a topic, return a dataframe w/ values"""

    output = scout_lab_input()
    if output:
        topic = output
    else:
        return

    query = """SELECT labs.title, topics.name AS topic, contacts.contact_name, contacts.email, labs.recruiting_status, labs.website FROM labs
               JOIN lab_x_topics ON labs.id = lab_x_topics.lab_id
               JOIN topics ON topics.id = lab_x_topics.topic_id
               LEFT JOIN contacts ON contacts.lab_id = labs.id WHERE topics.name = ?"""
    
    return pd.read_sql_query(query, connection, params=(topic,))


def add_lab(con: sqlite3.Connection):
    """Ask the user for new lab details and append them to the db"""

    # Gets title, restarts if title already exists. 
    output = add_lab_input()
    if output:
        title, topics, contact_name, contact_email, recruit_status, website = output
    else:
        return
        
    existing = con.execute("SELECT id FROM labs WHERE title = ?", (title,)).fetchone()
    if existing:
        print("Title already exists--lab not added.")
        return
    
    cursor = con.execute("INSERT INTO labs (title, website, recruiting_status) VALUES (?, ?, ?)", (title, website, recruit_status),)
    lab_id = cursor.lastrowid
 
    if contact_name or contact_email:
        con.execute("INSERT INTO contacts (lab_id, email, contact_name) VALUES (?, ?, ?)", (lab_id, contact_email, contact_name),)

    for topic in topics:
        topic_id, is_unique = check_lab_topics(con, topic)
        con.execute("INSERT OR IGNORE INTO lab_x_topics (lab_id, topic_id) VALUES (?, ?)", (lab_id, topic_id),)

    con.commit()
    print("Lab added.")
    return

def check_lab_topics(con: sqlite3.Connection, topic):
    """Check if topic entered already exists in database, add to db if not. Returns topic id and True if UNIQUE"""
    row = con.execute("SELECT id FROM topics WHERE name = ?", (topic,)).fetchone()
    if row:
        return row["id"], False
    cursor = con.execute("INSERT INTO topics (name) VALUES (?)", (topic,))
    return cursor.lastrowid, True
    

# main function
def main():
    connection = get_con()
    setup_db(connection)

    while True:
        choice = input("\nChoose from the following options:\n1. Search labs\n2. Add lab\n3. Options\n4. Quit\n-> ").strip()
 
        if choice == "1":
            print(scout_labs(connection))
        elif choice == "2":
            add_lab(connection)
        elif choice == "3":
            ask_migrate_or_clear(connection)
        elif choice == "4":
            connection.close()
            break
        else:
            print("Invalid choice, try again.")
 
 
if __name__ == "__main__":
    main()