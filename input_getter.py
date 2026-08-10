# Input prompter separate for the purpose of isoloating test cases.

def scout_lab_input():
    return input("Enter topic(s) to scout labs for.\n-> ")

def add_lab_input():
    title = input("Title: ").strip()

    topics = input("Topics (comma-separated): ").strip()
    if not title or not topics:
        print("Title and topics required--lab not added.")
        return
    topics = [topic.strip() for topic in topics.split(",") if topic.strip()]

    contact_name = input("Contact Name (optional): ").strip()
    contact_email = input("Contact Email (optional): ").strip()
    recruit_status = input("Recruiting Status (optional): ").strip()
    website = input("Website (optional): ").strip()

    return title, topics, contact_name, contact_email, recruit_status, website