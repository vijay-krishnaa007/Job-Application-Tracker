import pandas as pd
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "applications.csv")

os.makedirs(DATA_DIR, exist_ok=True)



def show_menu():
    print("\n=== Internship & Job Application Tracker ===")
    print("1. Add new application")
    print("2. View all applications")
    print("3. Update application status")
    print("4. Filter applications")
    print("5. Summary report")
    print("6. Exit")


def add_application():
    company = input("Enter company name: ").strip()
    role = input("Enter role applied for: ").strip()
    applied_date = input("Enter application date (YYYY-MM-DD): ").strip()

    print("Select application status:")
    statuses = ["Applied", "Interview", "Selected", "Rejected", "On Hold"]
    for i, status in enumerate(statuses, start=1):
        print(f"{i}. {status}")

    status_choice = input("Enter status number: ").strip()
    if not status_choice.isdigit() or not (1 <= int(status_choice) <= len(statuses)):
        print("Invalid status selection.")
        return

    status = statuses[int(status_choice) - 1]
    source = input("Enter application source: ").strip()
    follow_up_date = input("Enter follow-up date (YYYY-MM-DD): ").strip()

    new_record = {
        "company": company,
        "role": role,
        "applied_date": applied_date,
        "status": status,
        "source": source,
        "follow_up_date": follow_up_date
    }

    df = pd.DataFrame([new_record])
    file_exists = os.path.exists(DATA_FILE)
    df.to_csv(DATA_FILE, mode="a", header=not file_exists, index=False)

    print("Application added successfully.")

def view_applications():
    if not os.path.exists(DATA_FILE):
        print("No applications found.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("No applications to display.")
        return

    print("\n=== All Applications ===")
    print(df.to_string(index=False))

def filter_applications():
    if not os.path.exists(DATA_FILE):
        print("No applications found.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("No applications to filter.")
        return

    print("\nFilter by:")
    print("1. Status")
    print("2. Company")
    print("3. Role")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        statuses = ["Applied", "Interview", "Selected", "Rejected", "On Hold"]
        for i, status in enumerate(statuses, start=1):
            print(f"{i}. {status}")

        status_choice = input("Select status number: ").strip()
        if not status_choice.isdigit() or not (1 <= int(status_choice) <= len(statuses)):
            print("Invalid status selection.")
            return

        selected_status = statuses[int(status_choice) - 1]
        filtered_df = df[df["status"] == selected_status]

    elif choice == "2":
        company = input("Enter company name: ").strip()
        filtered_df = df[df["company"].str.lower() == company.lower()]

    elif choice == "3":
        role = input("Enter role name: ").strip()
        filtered_df = df[df["role"].str.lower() == role.lower()]

    else:
        print("Invalid filter option.")
        return

    if filtered_df.empty:
        print("No matching applications found.")
    else:
        print("\n=== Filtered Applications ===")
        print(filtered_df.to_string(index=False))

def update_application_status():
    if not os.path.exists(DATA_FILE):
        print("No applications found.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("No applications to update.")
        return

    print("\n=== Applications ===")
    print(df.reset_index().to_string(index=False))

    try:
        index = int(input("Enter index of application to update: ").strip())
    except ValueError:
        print("Invalid index.")
        return

    if index < 0 or index >= len(df):
        print("Index out of range.")
        return

    statuses = ["Applied", "Interview", "Selected", "Rejected", "On Hold"]
    print("\nSelect new status:")
    for i, status in enumerate(statuses, start=1):
        print(f"{i}. {status}")

    status_choice = input("Enter status number: ").strip()
    if not status_choice.isdigit() or not (1 <= int(status_choice) <= len(statuses)):
        print("Invalid status selection.")
        return

    new_status = statuses[int(status_choice) - 1]
    df.at[index, "status"] = new_status

    df.to_csv(DATA_FILE, index=False)
    print("Application status updated successfully.")

from datetime import datetime


def summary_report():
    if not os.path.exists(DATA_FILE):
        print("No applications found.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("No applications to summarize.")
        return

    print("\n=== Application Summary Report ===")

    # Total applications
    total = len(df)
    print(f"\nTotal Applications: {total}")

    # Status-wise count
    print("\nApplications by Status:")
    status_counts = df["status"].value_counts()
    for status, count in status_counts.items():
        print(f"{status}: {count}")

    # Follow-up analysis
    print("\nPending Follow-ups:")
    today = datetime.today().date()

    df["follow_up_date"] = pd.to_datetime(df["follow_up_date"], errors="coerce").dt.date
    pending_followups = df[df["follow_up_date"] >= today]

    if pending_followups.empty:
        print("No pending follow-ups.")
    else:
        print(pending_followups[["company", "role", "follow_up_date"]].to_string(index=False))






def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            update_application_status()
        elif choice == "4":
            filter_applications()
        elif choice == "5":
            summary_report()
        elif choice == "6":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
