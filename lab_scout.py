import pandas as pd
import sqlite3
from manage_db import setup_db, ask_migrate_or_clear

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 
def scout_labs():
    """Ask the user for a topic, return a dataframe w/ values"""

    connection = sqlite3.connect(DATABASE)

    topic = input("Enter topic(s) to scout labs for.\n-> ")

    query = """SELECT labs.title, topics.name AS topic, contacts.contact_name, contacts.email, labs.recruiting_status, labs.website FROM labs
               JOIN lab_x_topics ON labs.id = lab_x_topics.lab_id
               JOIN topics ON topics.id = lab_x_topics.topic_id
               LEFT JOIN contacts ON contacts.lab_id = labs.id WHERE topics.name = ?"""
    
    return pd.read_sql_query(query, connection, params=(topic,))



def add_lab():
    """Ask the user for new lab details and append them to the CSV."""
    title = input("Title: ").strip()
    topics = input("Topics (comma-separated): ").strip()
    contact_name = input("Contact Name: ").strip()
    contact_email = input("Contact Email: ").strip()
    recruit_status = input("Recruiting Status: ").strip()
    website = input("Website: ").strip()
 
    if not contact_name:
        contact_name = '-'
    if not contact_email:
        contact_email = '-'
    if not recruit_status:
        recruit_status = '-'
    if not website:
        website = '-'
        
    if not title or not topics:
        print("Title and topics required — lab not added.")
        return
 
    df = pd.read_csv(CSV_PATH)
    new_row = pd.DataFrame(
        [{'Title': title, 'Topics': topics, 'Contact Name': contact_name, 'Contact Email': contact_email, 'Recruiting Status': recruit_status, 'Website': website}],
        columns=df.columns
    )

    with open(CSV_PATH, 'rb+') as f:
        f.seek(0, 2)
        if f.tell() > 0:
            f.seek(-1, 2)
            if f.read(1) != b'\n':
                f.write(b'\n')

    new_row.to_csv(CSV_PATH, mode='a', index=False, header=False)
 
    print("Lab added.")



# main function
def main():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    setup_db()

    while True:
        choice = input("\nChoose from the following options:\n1. Search labs\n2. Add lab\n3. Options\n4. Quit\n-> ").strip()
 
        if choice == "1":
            print(scout_labs())
        elif choice == "2":
            add_lab()
        elif choice == "3":
            ask_migrate_or_clear()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")
 
 
if __name__ == "__main__":
    main()