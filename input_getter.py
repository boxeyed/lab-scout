# Input prompter separate for the purpose of isoloating test cases.
# Also handles cases and will be used for similar result searching

CHAR_LIMIT = 64

def scout_lab_input():
    return input("Enter topic(s) to scout labs for.\n-> ").strip().lower()

def add_lab_input():
    title = input("Title: ").strip().lower()

    topics = input("Topics (comma-separated): ").strip().lower()
    if not title or not topics:
        print("Title and topics required--lab not added.")
        return
    topics = [topic.strip().lower() for topic in topics.split(",") if topic.strip().lower()]

    contact_name = input("Contact Name (optional): ").strip().lower()
    contact_email = input("Contact Email (optional): ").strip().lower()
    recruit_status = input("Recruiting Status (optional): ").strip().lower()
    website = input("Website (optional): ").strip().lower()

    if not contact_name:
        contact_name = "Unknown"
    if len(contact_name) > CHAR_LIMIT:
        print("Character limit of 64 surpassed. Try again.")
        return
    
    if not contact_email:
        contact_email = "Unknown"
    if len(contact_email) > CHAR_LIMIT:
        print("Character limit of 64 surpassed. Try again.")
        return
    
    if not recruit_status:
        recruit_status = "Unknown"
    if len(recruit_status) > CHAR_LIMIT:
        print("Character limit of 64 surpassed. Try again.")
        return
    
    if not website:
        website = "Unknown"
    if len(website) > CHAR_LIMIT:
        print("Character limit of 64 surpassed. Try again.")
        return

    return title, topics, contact_name, contact_email, recruit_status, website