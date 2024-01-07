import os
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from colorama import Fore, Style, init
from prettytable import PrettyTable, FRAME, ALL


# Initialize colorama
init(autoreset=True)

# Constants
DATA_FILE = os.path.expanduser("~/.day_planner.json")


def print_title(title, end=""):
    print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{title}{Style.RESET_ALL}", end)


def print_error(message, end=""):
    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}{message}{Style.RESET_ALL}", end)


def print_success(message, end=""):
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{message}{Style.RESET_ALL}", end)


def print_warning(message, end=""):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}", end)


def print_info(message, end=""):
    print(f"{Fore.LIGHTCYAN_EX}{Style.NORMAL}{message}{Style.RESET_ALL}", end)


def print_primary(message, end=""):
    print(f"{Fore.YELLOW}{Style.NORMAL}{message}{Style.RESET_ALL}", end)


def print_prompt_and_warning(prompt, message, end=""):
    print(
        f"{prompt} {Fore.LIGHTYELLOW_EX}{Style.NORMAL}{message}{Style.RESET_ALL}", end
    )


# Functions
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {"tasks": []}


def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


def get_date_input(prompt, is_editing=False):
    while True:
        try:
            if is_editing:
                warning_message = "to set a new one press any key then press Enter"
                print_prompt_and_warning(prompt, warning_message)
                choice = input()

                if choice.strip() == "":
                    # User pressed Enter to keep existing
                    return None
                else:
                    # User pressed any other key then enter, continue with the menu
                    pass
            else:
                pass

            # Show options
            print_title("Date Input Options:")
            print("  1. today")
            print("  2. tomorrow")
            print("  3. in {?} days (e.g., 'in 2 days')")
            print("  4. next Monday")
            print("  5. next week")
            print("  6. in {?} weeks (e.g., 'in 2 weeks')")
            print("  7. next month")
            print("  8. in {?} months (e.g., 'in 2 months')")
            print("  9. other")

            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                return datetime.today().date()
            elif sub_choice == "2":
                return datetime.today().date() + timedelta(days=1)
            elif sub_choice == "3":
                days = int(input("\nEnter the number of days: "))
                return datetime.today().date() + timedelta(days=days)
            elif sub_choice == "4":
                next_monday = datetime.today() + timedelta(
                    days=(6 - datetime.today().weekday() + 1) % 7
                )
                return next_monday.date()
            elif sub_choice == "5":
                return datetime.today().date() + timedelta(weeks=1)
            elif sub_choice == "6":
                weeks = int(input("\nEnter the number of weeks: "))
                return datetime.today().date() + timedelta(weeks=weeks)
            elif sub_choice == "7":
                return (datetime.today() + relativedelta(months=1)).date()
            elif sub_choice == "8":
                months = int(input("\nEnter the number of months: "))
                return (datetime.today() + relativedelta(months=months)).date()
            elif sub_choice == "9":
                user_input = input(
                    "Enter the date (YYYY-MM-DD), in x days, in x weeks, or in x months (or leave empty to keep existing): "
                )
                if user_input.strip() == "":
                    return None
                elif user_input.lower().startswith("in "):
                    time_delta_str = user_input[3:].split()
                    if len(time_delta_str) == 2 and time_delta_str[1] in [
                        "days",
                        "weeks",
                        "months",
                    ]:
                        time_delta = int(time_delta_str[0])
                        if time_delta_str[1] == "days":
                            return datetime.today().date() + timedelta(days=time_delta)
                        elif time_delta_str[1] == "weeks":
                            return datetime.today().date() + timedelta(weeks=time_delta)
                        elif time_delta_str[1] == "months":
                            return (
                                datetime.today() + relativedelta(months=time_delta)
                            ).date()
                elif user_input.lower() == "today":
                    return datetime.today().date()
                elif user_input.lower() == "tomorrow":
                    return datetime.today().date() + timedelta(days=1)
                else:
                    return datetime.strptime(user_input, "%Y-%m-%d").date()
            else:
                print_error("Invalid choice. Please enter a number between 1 and 9.")
        except ValueError:
            print_error("Invalid input. Please try again.")


def get_duration_input(prompt, is_editing=False):
    while True:
        try:
            if is_editing:
                warning_message = "to set a new one press any key then press Enter"
                print_prompt_and_warning(prompt, warning_message)
                choice = input()

                if choice.strip() == "":
                    # User pressed Enter to keep existing
                    return None
                else:
                    # User pressed any other key then enter, continue with the menu
                    pass
            else:
                pass

            # Show options
            print_title("Duration Input Options:")
            print("  1. 15 minutes")
            print("  2. 30 minutes")
            print("  3. 45 minutes")
            print("  4. 1 hour")
            print("  5. 2 hours")
            print("  6. 3 hours")
            print("  7. other")

            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                return 15
            elif sub_choice == "2":
                return 30
            elif sub_choice == "3":
                return 45
            elif sub_choice == "4":
                return 60
            elif sub_choice == "5":
                return 120
            elif sub_choice == "6":
                return 180
            elif sub_choice == "7":
                duration = int(input("\nEnter the duration in minutes: "))
                return duration
            else:
                print_error("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print_error("Invalid input. Please try again.")

def list_tasks(tasks, completed=None, reverse=False):
    sorted_tasks = sorted(
        tasks["tasks"],
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
        reverse=reverse,
    )

    table = PrettyTable()
    table.field_names = ["#", "Title", "Due Date", "Duration", "Status"]
    table.hrules = ALL
    table.align["Title"] = "l"  # Align the "Title" column to the left


    for idx, task in enumerate(sorted_tasks):
        if completed is None or task["completed"] == completed:
            status = "Completed" if task["completed"] else "Incomplete"

            # Limit title and notes to 32 characters, append "..." if longer
            title = (task["title"][:29] + "...") if len(task["title"]) > 32 else task["title"]
            notes_line = (task.get("notes", "")[:29] + "...") if len(task.get("notes", "")) > 32 else task.get("notes", "")
            
            # Construct the second line only if notes is not empty
            title_notes = f"🏆 {title}\n📂 {notes_line}" if notes_line else title

            # Format due date to the desired format
            due_date = datetime.strptime(task["date"], "%Y-%m-%d").strftime("%a, %b %d, %Y")

            table.add_row(
                [
                    idx + 1,
                    title_notes,
                    due_date,
                    f"{task['duration']} minutes",
                    status,
                ]
            )

    print_title("\nTasks:")
    print(table)

def add_task(tasks):
    title = input("Task title: ")

    date_prompt = "Due date (YYYY-MM-DD, 'today', 'tomorrow', 'in x days', 'next week', 'in x weeks', 'next month', or 'in x months'): "
    date = get_date_input(date_prompt)

    while date is None:
        date = get_date_input("Due date cannot be empty. " + date_prompt)

    duration_prompt = "Planned duration (15, 30, 45, 60, 120, 180 minutes, or 'other' for custom duration): "
    duration = get_duration_input(duration_prompt)

    while duration is None:
        duration = get_duration_input("Duration cannot be empty. " + duration_prompt)

    notes = input("Task notes (additional information): ")

    new_task = {
        "title": title,
        "date": str(date),
        "duration": duration,
        "completed": False,
        "notes": notes,
        "completed_at": None,
    }
    tasks["tasks"].append(new_task)
    save_tasks(tasks)
    print_success(f"\nTask added successfully.")

def edit_task(tasks):
    list_tasks(tasks, False, True)
    try:
        task_index = int(input("\nEnter the task number to edit: ")) - 1
        if 0 <= task_index < len(tasks["tasks"]):
            task = tasks["tasks"][task_index]
            print(
                f"\nEditing task: {task['title']} ({task['date']}, {task['duration']} minutes)"
            )

            title = input("New task title (leave empty to keep existing): ")
            if title:
                task["title"] = title

            date = get_date_input("New due date (leave empty to keep existing): ", True)
            if date:
                task["date"] = str(date)

            duration = get_duration_input(
                "New planned duration (leave empty to keep existing): ", True
            )
            if duration:
                task["duration"] = duration

            notes = input(
                "New task notes (additional information, leave empty to keep existing): "
            )
            if notes:
                task["notes"] = notes

            save_tasks(tasks)
            print_success(f"\nTask edited successfully.")
        else:
            print_error("Invalid task number.")
    except ValueError:
        print_error("Invalid input. Please enter a valid task number.")

def remove_task(tasks):
    list_tasks(tasks, reverse=True)
    try:
        task_index = int(input("\nEnter the task number to remove: ")) - 1
        if 0 <= task_index < len(tasks["tasks"]):
            removed_task = tasks["tasks"].pop(task_index)
            save_tasks(tasks)
            print_success(f"\nTask '{removed_task['title']}' removed successfully.")
        else:
            print_error("Invalid task number.")
    except ValueError:
        print_error("Invalid input. Please enter a valid task number.")

def mark_task_done(tasks):
    list_tasks(tasks, False, True)
    try:
        task_index = int(input("\nEnter the task number to mark as done: ")) - 1
        if 0 <= task_index < len(tasks["tasks"]):
            tasks["tasks"][task_index]["completed"] = True
            tasks["tasks"][task_index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print_success(
                f"\nTask '{tasks['tasks'][task_index]['title']}' marked as done at {tasks['tasks'][task_index]['completed_at']}."
            )
        else:
            print_error("Invalid task number.")
    except ValueError:
        print_error("Invalid input. Please enter a valid task number.")

def view_task_details(tasks):
    list_tasks(tasks, reverse=True)
    try:
        task_index = int(input("\nEnter the task number to view details: ")) - 1
        if 0 <= task_index < len(tasks["tasks"]):
            task = tasks["tasks"][task_index]
            print("\nTask Details:")
            print(f"Title: {task['title']}")
            print(f"Due Date: {task['date']}")
            print(f"Planned Duration: {task['duration']} minutes")
            print(f"Status: {'Completed' if task['completed'] else 'Incomplete'}")

             # Display completed_at if available
            if task.get("completed_at"):
                print(f"Completed At: {task['completed_at']}")

            print(f"Notes: {task.get('notes', '')}")
        else:
            print_error("Invalid task number.")
    except ValueError:
        print_error("Invalid input. Please enter a valid task number.")


# Modify the main function
def main():
    tasks = load_tasks()

    list_tasks(tasks, False, True)

    try:
        while True:
            print_title("\nOptions:")
            print_info("1. Add Task")
            print_info("2. Edit Task")
            print_info("3. Remove Task")
            print_info("4. List Tasks (Newest to Oldest)")
            print_info("5. List Completed Tasks (Newest to Oldest)")
            print_info("6. Mark Task as Done")
            print_info("7. View Task Details")
            print_info("8. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                edit_task(tasks)
            elif choice == "3":
                remove_task(tasks)
            elif choice == "4":
                list_tasks(tasks, completed=False, reverse=True)
            elif choice == "5":
                list_tasks(tasks, completed=True, reverse=True)
            elif choice == "6":
                mark_task_done(tasks)
            elif choice == "7":
                view_task_details(tasks)
            elif choice == "8":
                print_info("Exiting the day planner app.")
                break
            else:
                print_error("Invalid choice. Please enter a number between 1 and 8.")
    except KeyboardInterrupt:
        print_info("\nExiting the day planner app.")


if __name__ == "__main__":
    main()
