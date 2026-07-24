import pandas as pd
import sqlite3
from manage_db import get_connection, setup_db, ask_migrate_or_clear

CSV_PATH = "data.csv"
DATABASE = "labs.db"
 

def load_records():
    """Read the CSV and migrate its values to the db (one-time)."""
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient='records')

def scout_labs():
    """Ask the user for a topic, print matching labFls."""
    records = load_records()
    topic = input("Enter a topic to search for: ").strip()
 
    matches = []
    for record in records:
        topics_list = [t.strip() for t in record['Topics'].split(',')]
        if topic in topics_list:
            matches.append(record)
 
    if matches:
        for record in matches:
            print(f"\nTitle: {record['Title']}")
            print(f"Topics: {record['Topics']}")
            print(f"Contact Name: {record['Contact Name']}")
            print(f"Contact Email: {record['Contact Email']}")
            print(f"Recruiting Status: {record['Recruiting Status']}")
            print(f"Website: {record['Website']}")
    else:
        print("No matches found.")


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
            scout_labs()
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