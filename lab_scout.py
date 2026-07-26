import pandas as pd
import sqlite3
from manage_db import setup_db, ask_migrate_or_clear, get_con

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 
def scout_labs(connection: sqlite3.Connection):
    """Ask the user for a topic, return a dataframe w/ values"""

    topic = input("Enter topic(s) to scout labs for.\n-> ")

    query = """SELECT labs.title, topics.name AS topic, contacts.contact_name, contacts.email, labs.recruiting_status, labs.website FROM labs
               JOIN lab_x_topics ON labs.id = lab_x_topics.lab_id
               JOIN topics ON topics.id = lab_x_topics.topic_id
               LEFT JOIN contacts ON contacts.lab_id = labs.id WHERE topics.name = ?"""
    
    return pd.read_sql_query(query, connection, params=(topic,))



def add_lab(con: sqlite3.Connection):
    """Ask the user for new lab details and append them to the db"""
    title = input("Title: ").strip()
    topics = input("Topics (comma-separated): ").strip()
    if not title or not topics:
        print("Title and topics required--lab not added.")
        return
    topics = topics.split(",")

    contact_name = input("Contact Name (optional): ").strip()
    contact_email = input("Contact Email (optional): ").strip()
    recruit_status = input("Recruiting Status (optional): ").strip()
    website = input("Website (optional): ").strip()
 
    if not contact_name:
        contact_name = None
    if not contact_email:
        contact_email = None
    if not recruit_status:
        recruit_status = "Unknown"
    if not website:
        website = None
        
 
    existing = con.execute("SELECT id FROM labs WHERE title = ?", (title,)).fetchone()
    # Title already exists, duplicate not added. 
    if existing==True:
        return
    
    cursor = con.execute("INSERT INTO labs (title, website, recruiting_status) VALUES (?, ?, ?)", (title, website, recruit_status),)
    lab_id = cursor.lastrowid
 
    if contact_name or contact_email:
        con.execute("INSERT INTO contacts (lab_id, email, contact_name) VALUES (?, ?, ?)", (lab_id, contact_email, contact_name),)
 
    con.commit()
    print("Lab added.")
    return



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
            ask_migrate_or_clear()
        elif choice == "4":
            connection.close()
            break
        else:
            print("Invalid choice, try again.")
 
 
if __name__ == "__main__":
    main()