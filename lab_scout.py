import pandas as pd
 
CSV_PATH = "data.csv"
 
 
def load_records():
    """Read the CSV and return a list of row dictionaries."""
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient='records')

def scout_labs():
    """Ask the user for a topic, print matching labs."""
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
            print(f"Description: {record['Description']}")
    else:
        print("No matches found.")


def add_lab():
    """Ask the user for new lab details and append them to the CSV."""
    title = input("Title: ").strip()
    topics = input("Topics (comma-separated): ").strip()
    description = input("Description: ").strip()
 
    if not title or not topics or not description:
        print("All fields are required — lab not added.")
        return
 
    df = pd.read_csv(CSV_PATH)
    new_row = pd.DataFrame(
        [{'Title': title, 'Topics': topics, 'Description': description}],
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
    while True:
        print("\n1. Search labs")
        print("2. Add lab")
        print("3. Quit")
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            scout_labs()
        elif choice == "2":
            add_lab()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")
 
 
if __name__ == "__main__":
    main()