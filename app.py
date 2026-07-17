import pandas as pd
 
CSV_PATH = "sample_data.csv"
 
 
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

# main function
def main():
    while True:
        print("\n1. Search labs")
        print("2. Quit")
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            scout_labs()
        elif choice == "2":
            break
        else:
            print("Invalid choice, try again.")
 
 
if __name__ == "__main__":
    main()