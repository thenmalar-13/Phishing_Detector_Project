import csv
import random
import re
from datetime import datetime

# Load emails from CSV
def load_emails(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# Simple red flag checks
def check_red_flags(email_text):
    red_flags = []

    # Suspicious links (IP address or strange domain)
    if re.search(r"http[s]?://(?:\d{1,3}\.){3}\d{1,3}", email_text):
        red_flags.append("IP-based URL")

    if re.search(r"(faceb00k|paypa1|amaz0n|click here|free)", email_text, re.I):
        red_flags.append("Misspelled or fake domain/phrases")

    # Urgent language
    if re.search(r"(urgent|verify|reset|account suspended|win)", email_text, re.I):
        red_flags.append("Urgent tone")

    return red_flags

# Ask user and give feedback
def run_session(email):
    print("\n📩 Email: ", email['email_text'])
    user_input = input("👉 Is this email safe? (Y/N): ").strip().upper()

    correct_label = email['label']
    is_correct = (user_input == 'Y' and correct_label == 'genuine') or \
                 (user_input == 'N' and correct_label == 'phishing')

    flags = check_red_flags(email['email_text'])

    # Feedback
    if is_correct:
        print("✅ Correct!")
    else:
        print("❌ Incorrect.")

    print("📌 Reason(s):", ", ".join(flags) if flags else "No phishing indicators found.")

    # Logging
    log_decision(email['id'], user_input, correct_label, is_correct, flags)

def log_decision(email_id, user_input, actual_label, correct, flags):
    with open("log.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(), email_id, user_input, actual_label,
            "Correct" if correct else "Wrong", ";".join(flags)
        ])

# Main
def main():
    emails = load_emails("emails.csv")
    email = random.choice(emails)
    run_session(email)

if __name__ == "__main__":
    # Create log file with headers if it doesn't exist
    try:
        with open("log.csv", "x", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Email_ID", "User_Response", "Actual_Label", "Result", "Red_Flags"])
    except FileExistsError:
        pass

    main()
