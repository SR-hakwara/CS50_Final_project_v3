import sys
from tabulate import tabulate
from datetime import date
from controller import *
import re

# this file was reformated by black module


def main() -> None:
    """
    - Main application loop providing a menu-driven interface for managing projects and tasks.
    Allows users to:
        - Manage projects (view, add, update, delete)
        - Manage tasks (view, add, update, delete)
        - Exit the application
    """
    try:  # catch CTRL+D and print an exit message
        while True:
            project_list: Projects = Projects()
            task_list: Tasks = Tasks()  # Object Tasks

            print(get_general_option())
            choice_g: str = input("Choose an option: ").strip()
            match choice_g:
                case "1":
                    # Project management submenu

                    while True:
                        print(get_project_option())
                        choice_project = input("Choose an option: ").strip()
                        match choice_project:
                            case "1":
                                # Display all projects
                                print(view_all(project_list))
                                input("Press Enter to continue ➡️ ... ")
                            case "2":
                                # Display single project details
                                print(view_single_data(project_list))
                                input("Press Enter to continue ➡️ ... ")
                            case "3":
                                # Add a new project
                                add_data(project_list)
                                input("Press Enter to continue ➡️ ... ")
                            case "4":
                                # Update project
                                update_data(project_list, task_list)
                            case "5":
                                # Delete project
                                delete_data(project_list, task_list)
                            case "6":
                                # Return to the main menu
                                break
                            case "7":
                                # Exit application
                                sys.exit()
                            case _:
                                # Handle invalid option
                                print(invalid_option())
                                input("Press Enter to continue ➡️ ... ")
                        ...
                case "2":
                    # Task management submenu
                    while True:
                        print(get_task_option())
                        choice_task: str = input("Choose an option: ").strip()
                        match choice_task:
                            case "1":
                                # Display all tasks
                                print(view_all(task_list))
                                input("Press Enter to continue ➡️ ... ")
                            case "2":
                                # Display single task details
                                print(view_single_data(task_list))
                                input("Press Enter to continue ➡️ ... ")
                            case "3":
                                # Add a new task
                                add_data(task_list)
                                input("Press Enter to continue ➡️ ... ")
                            case "4":
                                # Update task
                                update_data(task_list, project_list)
                            case "5":
                                # Delete task
                                delete_data(task_list, project_list)
                            case "6":
                                # Return to the main menu
                                break
                            case "7":
                                # Exit application
                                sys.exit()
                            case _:
                                # Handle invalid option
                                print(invalid_option())
                                input("Press Enter to continue ➡️ ... ")
                case "3":
                    # Exit application
                    print("Goodbye! See you soon !! =)")
                    break
                case _:
                    # Handle invalid option
                    print(invalid_option())
                    input("Press Enter to continue ➡️ ... ")
        sys.exit()
    except EOFError:
        print("Goodbye! See you soon !! =)")
        sys.exit()


def view_all(data_list: Data) -> str:
    """
    Retrieve and display all objects from a given list in a tabular format with tabulate module.
    Args:
        data_list : Data [Projects or Tasks]: List of projects or tasks to display
    Returns:
        str: Tabulated data with tabulate module or error message
    """
    try:
        data_: list = []
        data_list.data_from_csv()
        for object_ in data_list.objects:
            # Create a copy to avoid modifying the original object
            obj_dict: dict = object_.__dict__.copy()
            # Exclude detailed description from overview
            obj_dict.pop("detailed_description", None)
            data_.append(obj_dict)
        return tabulate(data_, headers="keys", tablefmt="grid", maxcolwidths=30)
    except ValueError as e:
        print(e)
        return ""


def view_single_data(data_list):
    """
    Display details of a single object by its ID.
    Args:
        data_list : Data [Projects or Tasks]: List of projects or tasks.
    Returns:
       str: display a single object with tabulate module or error message.
    """

    try:
        data_list.data_from_csv()
        id_ = input(f"➡️ Enter the {data_list.data_type} id you want to view: ")
        object_ = data_list.get_object(id_)
        data_ = [object_.__dict__]
        single_data = tabulate(data_, headers="keys", tablefmt="grid", maxcolwidths=30)
        # If the displayed object is a project, display its linked tasks as well if they exist.
        if data_list.data_type == "project":
            linked_tasks = []
            data_task = Tasks()
            try:
                data_task.data_from_csv()
                for task_id in object_.task_list:
                    linked_tasks.append(data_task.get_object(task_id).convert_to_dict())
                if linked_tasks:
                    tasks_display = tabulate(
                        linked_tasks, headers="keys", tablefmt="grid", maxcolwidths=30
                    )
                    single_data += "\n\nProject Tasks:\n" + tasks_display
            except ValueError:
                ...
        return single_data

    except ValueError as e:
        print(e)
        return ""


def add_data(data_list) -> None:
    """
    Add a new project or task to the data_list.
    We don't use objects in this case but just data_list.data.
    Args:
        data_list : Data [Projects or Tasks]: List to add data to
    Returns:
        None
    """
    try:
        data_list.data_from_csv()
    except ValueError:
        data_list.data = []

    id_ = new_id(data_list)
    data_input = {
        "id": id_,
        "name": input(f"➡️ Enter {data_list.data_type} name: ").strip(),
        "description": input(
            f"➡️ Entrer a short description for the {data_list.data_type}: "
        ).strip(),
        "detailed_description": input(
            f"➡️ Enter a detailed description for the {data_list.data_type}: "
        ).strip(),
        "creation_date": date.today(),
    }
    # Validate deadline with maximum 3 attempts
    compter = 0
    while compter < 3:
        dead_line = input("➡️ Enter dead line (YYYY-MM-DD ie:2024-12-31): ")
        if is_valid_deadline(dead_line):
            data_input["dead_line"] = dead_line
            break
        else:
            print(
                "⚠️ Deadline must be today or later, and in the format (YYYY-MM-DD, e.g., 2025-01-30) ⚠️"
            )
            compter += 1
    if compter == 3:
        print("⚠️ 3 wrong attempt start again ⚠️")
        return
    data_input["state"] = "To do"
    if data_list.data_type == "project":
        data_input["task_list"] = []
    elif data_list.data_type == "task":
        data_input["linked_project"] = ""

    data_list.data.append(data_input)
    data_list.data_to_csv()


def update_data(data_list_1, data_list_2) -> None:
    """
    we import both projects and tasks to allow change of task_list and project_linked in same time
    Update an existing project or task, potentially modifying related data (task list and linked project).
    Args:
        data_list_1 (Data [Projects or Tasks]): Primary data list to update
        data_list_2 (Data [Projects or Tasks]): Secondary data list for updated related property
    Returns:
        None
    """
    try:  #
        data_list_1.data_from_csv()
        try:
            data_list_2.data_from_csv()
        except ValueError:
            data_list_2.data = []
        # Get an object to update
        id_ = input(f"Enter {data_list_1.data_type} ID you want to update: ")
        data_ = data_list_1.get_object(id_)
        print(
            tabulate([data_.__dict__], headers="keys", tablefmt="grid", maxcolwidths=30)
        )
        # Choose property to update
        property_ = input(" 🔄 Which Property you want to update ?: ").strip()
        # id the object data_ has attribut property_
        if hasattr(data_, property_):
            # Special handling for task_list updates
            if property_ == "task_list":
                print(f"list of task : {data_list_2.get_all_ids()}")
                used_task = [
                    item
                    for sublist in data_list_1.get_all_property_value("task_list")
                    for item in sublist
                ]
                print(f"already used_tasks={used_task}")
                value = input(
                    "Enter the new value of task you want to add to this project: "
                ).strip()
                # Validate task usage in another project
                if not value in data_.task_list and value in used_task:
                    raise ValueError(f"⚠️ this task is already used in other project ⚠️")
                if value in data_.task_list:
                    # ask for Removing a task from the project if the task is already in task_list
                    confirm = (
                        input(
                            f"⚠️ this task is already in task_list ⚠️ you want to delete it ? (yes/no): "
                        )
                        .strip()
                        .lower()
                    )
                    if confirm in ["yes", "y"]:
                        # remove the task from the project task list
                        data_.task_list.remove(value)
                        # delete project id from linked_project for the task removed
                        data_list_2.get_object(value).linked_project = ""
                        save_change(data_list_1)
                        save_change(data_list_2)
                    else:
                        raise ValueError("🔴 the update has been canceled 🔴")
                else:
                    # add the task into the task list
                    data_.task_list += [value]
                    # add the project id to the task linked project
                    data_list_2.get_object(value).linked_project = id_
                    save_change(data_list_1)
                    save_change(data_list_2)
            # Special handling for linked_project updates
            elif property_ == "linked_project":
                raise ValueError(
                    "🔴 to update the task linked_project go to project and update task_list 🔴"
                )
            # Update any other properties
            else:
                value = input("Enter the new value: ").strip()
                setattr(data_, property_, value)
                save_change(data_list_1)
            print(f"🟢 The property '{property_}' has been updated successfully! 🟢")
        else:
            print(
                f"🔴 The property '{property_}' does not exist in the {data_list_1.data_type} 🔴"
            )
    except ValueError as e:
        print(e)


def delete_data(data_list_1, data_list_2) -> None:
    """
    Delete a project or task and handle related dependencies.
    Args:
        data_list_1 (Data [Projects or Tasks]): Primary data list to delete from
        data_list_2 (Data [Projects or Tasks]): Secondary data list for deleting the id from task_list if linked_project
    Returns:
        None
    """
    try:
        data_list_1.data_from_csv()
        id_ = input(
            f"enter the {data_list_1.data_type} ID you want to delete: "
        ).strip()
        object_ = data_list_1.get_object(id_)
        data_ = [object_.convert_to_dict()]
        print(tabulate(data_, headers="keys", tablefmt="grid", maxcolwidths=30))
        # Confirm and delete the object
        confirmer = (
            input(f"Are You sur you want delete this {data_list_1.data_type} (yes/no: ")
            .strip()
            .lower()
        )
        if confirmer in ["yes", "y"]:
            # Delete the object
            data_list_1.delete_object(object_)
            save_change(data_list_1)
            try:
                # Handle related objects
                if data_list_1.data_type == "project":
                    try:  # if a task linked to this project, delete "linked_project" property value
                        data_list_2.data_from_csv()
                        ob1 = data_list_2.get_object_by_property_value(
                            "linked_project", id_
                        )
                        setattr(ob1, "linked_project", "")
                        save_change(data_list_2)
                    except ValueError:
                        ...
                if data_list_1.data_type == "task":
                    try:  # if a project have this task in task_list, remove the task id
                        data_list_2.data_from_csv()
                        ob2 = data_list_2.get_object_by_property_value("task_list", id_)
                        ob2.task_list.remove(id_)
                        save_change(data_list_2)
                    except ValueError:
                        ...
            except ValueError as e:
                print(e)

            print(f"🟢 your {data_list_1.data_type} has been deleted successfully 🟢")
        else:
            print("🔴 the deletion has been canceled 🔴")
    except ValueError as e:
        print(e)


def save_change(data_list) -> None:
    """
    Save changes to the data list by updating objects to data_list.data and writing to CSV.
    Args:
        data_list (Data[Projects or Tasks]): Data list to save
    """
    try:
        data_list.set_objects()
        data_list.data_to_csv()
    except ValueError as e:
        print(e)


def new_id(list_: Data) -> str:
    """
    this way to generate ID, allow us to reuse ID if the project or the task are deleted
    otherwise we could use new_id=max(all_ids)+1
    Args:
        list_ (Data): Data list to check existing IDs
    Returns:
        str: A new unique ID
    """
    all_ids = list_.get_all_ids()
    new_id_: int = 1
    while new_id_ in all_ids:
        new_id_ += 1
    return str(new_id_)


def is_valid_deadline(dead_line: str, today: date = date.today()) -> bool:
    """
    Validate deadline format YYYY-MM-DD and ensure it is not in the past.
    Args:
        dead_line (str): Deadline date string
        today (date, optional for testing purpose): Reference date for validation. Defaults to today.
    Returns:
        bool: True if deadline is valid, False otherwise
    """

    pattern = (
        r"^(?P<Year>20[2-9][0-9])-(?P<Month>0[0-9]|1[0-2])-(?P<DD>[0-2][0-9]|3[0-1])$"
    )
    match = re.match(pattern, dead_line)
    if match and today <= date.fromisoformat(dead_line):
        return True
    return False


def get_general_option():

    return """what do you want to do?
    1. 🎯 Manage your projects.
    2. ✅ Manage your tasks.
    3. ❌ Exit()
          """


def get_project_option():
    return """What do you want to do?
    1. 👁️ Display projects
    2. 👁️ Display a project with id
    3. ➕ Add project
    4. 🔄 Update project
    5. ➖ Delete project
    6. 🔙 Back
    7. ❌ Exit
    """


def get_task_option():
    return """What do you want to do?
    1. 👁️ Display tasks
    2. 👁️ Display a task with id
    3. ➕ Add task
    4. 🔄 Update task
    5. ➖ Delete task
    6. 🔙 Back
    7. ❌ Exit
    """


def invalid_option() -> str:
    return "⚠️ Invalid option. Please try again. ⚠️"


if __name__ == "__main__":
    main()
