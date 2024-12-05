import sys
from tabulate import tabulate
from datetime import date
from controller import *
import re

# this file was reformated by black module

S = "\033[1m"  # start bold
E = "\033[0m"  # end bold


def main() -> None:
    """
    - Main application loop providing a menu-driven interface for managing projects and tasks.
    - Allows users to:
        - Manage projects (view, add, update, delete)
        - Manage tasks (view, add, update, delete)
        - Exit the application
    """
    try:  # catch CTRL+D and print an exit message
        print(
            f"""\n\033[92m★★★{E} {S} Welcome to CS50 Project{E} \033[92m★★★{E}
\033[92m▶▶{E} {S} Project and Tasks Management{E} \033[92m◀◀{E}"""
        )
        while True:
            project_list: Projects = Projects()
            task_list: Tasks = Tasks()  # Object Tasks

            print(get_general_option())
            choice_g: str = input(f"🔵 {S}Choose an option: {E}").strip()
            match choice_g:
                case "1":
                    # Project management submenu

                    while True:
                        print(get_project_option())
                        choice_project = input(f"🔵 {S}Choose an option: {E}").strip()
                        match choice_project:
                            case "1":
                                # Display all projects
                                print(view_all(project_list))
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                            case "2":
                                # Display single project details
                                print(view_single_data(project_list))
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                            case "3":
                                # Add a new project
                                add_data(project_list)
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
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
                                print(f"\n👋👋 {S} Goodbye! See you soon !!{E}🙂\n")
                                sys.exit()
                            case _:
                                # Handle invalid option
                                print(invalid_option())
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                        ...
                case "2":
                    # Task management submenu
                    while True:
                        print(get_task_option())
                        choice_task: str = input(f"{S}🔵 Choose an option: {E}").strip()
                        match choice_task:
                            case "1":
                                # Display all tasks
                                print(view_all(task_list))
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                            case "2":
                                # Display single task details
                                print(view_single_data(task_list))
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                            case "3":
                                # Add a new task
                                add_data(task_list, project_list)
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
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
                                print(f"\n👋👋 {S} Goodbye! See you soon !!{E}🙂\n")
                                sys.exit()
                            case _:
                                # Handle invalid option
                                print(invalid_option())
                                input(f"{S}Press Enter to continue ➡️  ... {E}")
                case "3":
                    # Exit application
                    print(f"\n👋👋 {S} Goodbye! See you soon !!{E}🙂\n")
                    break
                case _:
                    # Handle invalid option
                    print(invalid_option())
                    input(f"{S}Press Enter to continue ➡️  ... ")
        sys.exit()
    except EOFError:
        print(f"\n\n👋👋 {S} Goodbye! See you soon !!{E}🙂\n")
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
        id_ = input(f"➡️  Enter the {data_list.data_type} id you want to view: ").strip()
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
                    task = data_task.get_object(task_id).convert_to_dict()
                    task.pop("detailed_description", None)
                    linked_tasks.append(task)
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


def add_data(data_list, project_list=None) -> None:
    """
    Add a new project or task to the data_list.
    We don't use objects in this case but just data_list.data.
    Args:
        data_list : Data [Projects or Tasks]: List to add data to
        project_list : If data is a Task we import project too, to update it if linked_project is added
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
        "name": input(f"➡️  Enter {data_list.data_type} name: ").strip(),
        "description": input(
            f"➡️  Entrer a short description for the {data_list.data_type}: "
        ).strip(),
        "detailed_description": input(
            f"➡️  Enter a detailed description for the {data_list.data_type}: "
        ).strip(),
        "creation_date": date.today(),
    }
    # Validate deadline with maximum 3 attempts
    compter = 0
    while compter < 3:
        deadline = input("➡️  Enter deadline (YYYY-MM-DD ie:2024-12-31): ").strip()
        if is_valid_deadline(deadline):
            data_input["deadline"] = deadline
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
        confirmation = (
            input("➡️  you want to link this task to a existing project?(yes/no): ")
            .strip()
            .lower()
        )
        if not confirmation in ["yes", "y"]:
            data_input["linked_project"] = ""
        else:
            project_list.data_from_csv()
            available_project = []
            for project in project_list.objects:
                available_project.append(f"{project.id}: {project.name} ")
            print(f"Available projects : {available_project}")
            compter_id = 0
            while compter_id < 3:
                try:
                    project_id = int(
                        input(
                            "➡️  Enter the ID of the project you want to add to this task: "
                        ).strip()
                    )
                    print(f"all ids: {project_list.get_all_ids()}")
                    if project_id in project_list.get_all_ids():
                        print(project_id)
                        data_input["linked_project"] = str(project_id)
                        project_list.get_object(str(project_id)).task_list += [id_]
                        save_change(project_list)
                        break
                    else:
                        print("⚠️  No project with this ID ⚠️")
                        compter_id += 1
                except ValueError as e:
                    print(e)
                    print("⚠️  Invalid input. Please enter a numeric ID. ⚠️")
                    compter_id += 1
            if compter_id == 3:
                print("⚠️ 3 wrong attempt start again ⚠️")
                return
    print(
        f"🟢 your {data_list.data_type} has been added successfully with ID = {id_} 🟢"
    )
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
        id_ = input(f"➡️  Enter {data_list_1.data_type} ID you want to update: ").strip()
        data_ = data_list_1.get_object(id_)
        print(
            tabulate([data_.__dict__], headers="keys", tablefmt="grid", maxcolwidths=30)
        )
        # Choose property to update
        compteur = 0
        while compteur < 3:
            property_o = (
                input("🔄  Which Property you want to update ?: ").strip().lower()
            )
            property_ = ""
            if property_o.find(" "):
                property_ = property_o.replace(" ", "_")
            # id the object data_ has attribut property_
            if hasattr(data_, property_):
                # Special handling for task_list updates
                if property_ == "task_list":
                    compteur_err_task = 0
                    all_task_ids = data_list_2.get_all_ids()
                    used_task = [
                        item
                        for sublist in data_list_1.get_all_property_value("task_list")
                        for item in sublist
                    ]
                    used_task_int = [int(task) for task in used_task]
                    available_task_id = list(set(all_task_ids) - set(used_task_int))
                    available_task = []
                    for id_task in available_task_id:
                        available_task.append(
                            f"{id_task}: {data_list_2.get_object(str(id_task)).name}"
                        )
                    while compteur_err_task < 3:
                        print(f"📋  list of available task : {available_task}")
                        value = input(
                            "➡️  Enter the ID of the task you want to add to this project: "
                        ).strip()
                        # Validate task usage in another project
                        if not value in data_.task_list and value in used_task:
                            print(f"⚠️ This task is already used in other project ⚠️")
                            compteur_err_task += 1
                        elif value in data_.task_list:
                            # ask for Removing a task from the project if the task is already in task_list
                            confirm = (
                                input(
                                    f"⚠️ This task is already in task_list ⚠️ you want to delete it ? (yes/no)❓: "
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
                                break
                            else:
                                raise ValueError("🔴  The update has been canceled 🔴")
                        elif not value.isnumeric() or not int(value) in all_task_ids:
                            print(f"⚠️  No task with this ID ⚠️")
                            compteur_err_task += 1
                        else:
                            # add the task into the task list
                            data_.task_list += [value]
                            # add the project id to the task linked project
                            data_list_2.get_object(value).linked_project = id_
                            save_change(data_list_1)
                            save_change(data_list_2)
                            break
                    if compteur_err_task == 3:
                        print("⚠️ 3 wrong attempt start again ⚠️")
                        break
                # Special handling for linked_project updates
                elif property_ == "linked_project":
                    if data_.linked_project == "":
                        available_project = []
                        for project in data_list_2.objects:
                            available_project.append(f"{project.id}: {project.name} ")
                        print(f"Available projects : {available_project}")
                        compter_id = 0
                        while compter_id < 3:
                            try:
                                project_id = int(
                                    input(
                                        "➡️  Enter the ID of the project you want to add to this task: "
                                    ).strip()
                                )
                                print(f"all ids: {data_list_2.get_all_ids()}")
                                if project_id in data_list_2.get_all_ids():
                                    print(project_id)
                                    data_.linked_project = str(project_id)
                                    data_list_2.get_object(
                                        str(project_id)
                                    ).task_list += [id_]
                                    save_change(data_list_2)
                                    save_change(data_list_1)
                                    break
                                else:
                                    print("⚠️  No project with this ID ⚠️")
                                    compter_id += 1
                            except ValueError as e:
                                print(e)
                                print("⚠️  Invalid input. Please enter a numeric ID. ⚠️")
                                compter_id += 1
                        if compter_id == 3:
                            print("⚠️ 3 wrong attempt start again ⚠️")
                            return
                    else:
                        raise ValueError(
                            "🔴  A project is already linked to this task. To update the task linked_project go to project and update task_list 🔴"
                        )
                elif property_ == "deadline":
                    compter_deadline = 0
                    while compter_deadline < 3:
                        deadline = input("➡️  Enter deadline (YYYY-MM-DD ie:2024-12-31): ").strip()
                        if is_valid_deadline(deadline):
                            setattr(data_, property_, deadline)
                            save_change(data_list_1)
                            break
                        else:
                            print(
                                "⚠️ Deadline must be today or later, and in the format (YYYY-MM-DD, e.g., 2025-01-30) ⚠️"
                            )
                            compter_deadline += 1
                    if compter_deadline == 3:
                        print("⚠️ 3 wrong attempt start again ⚠️")
                        return

                elif property_ == "id":
                    raise ValueError("🔴  You can't modify the id 🔴")
                # Update any other properties
                else:
                    value = input("➡️  Enter the new value: ").strip()
                    setattr(data_, property_, value)
                    save_change(data_list_1)
                print(
                    f"🟢  The property '{property_}' has been updated successfully! 🟢"
                )
                break
            else:
                compteur += 1
                print(
                    f"🔴  The property '{property_}' does not exist in the {data_list_1.data_type} 🔴"
                )
        if compteur == 3:
            print("⚠️ 3 wrong attempt start again ⚠️")
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
            f"➡️  Enter the {data_list_1.data_type} ID you want to delete: "
        ).strip()
        object_ = data_list_1.get_object(id_)
        data_ = [object_.convert_to_dict()]
        print(tabulate(data_, headers="keys", tablefmt="grid", maxcolwidths=30))
        # Confirm and delete the object
        confirmer = (
            input(
                f"⚠️  Are You sur you want delete this {data_list_1.data_type} (yes/no)❓: "
            )
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

            print(f"🟢  Your {data_list_1.data_type} has been deleted successfully 🟢")
        else:
            print("🔴  The deletion has been canceled 🔴")
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


def is_valid_deadline(deadline: str, today: date = date.today()) -> bool:
    """
    Validate deadline format YYYY-MM-DD and ensure it is not in the past.
    Args:
        deadline (str): Deadline date string
        today (date, optional for testing purpose): Reference date for validation. Defaults to today.
    Returns:
        bool: True if deadline is valid, False otherwise
    """

    pattern = (
        r"^(?P<Year>20[2-9][0-9])-(?P<Month>0[0-9]|1[0-2])-(?P<DD>[0-2][0-9]|3[0-1])$"
    )
    match = re.match(pattern, deadline)
    try:
        if match and today <= date.fromisoformat(deadline):
            return True
        else:
            return False
    except ValueError as e:
        print(e)
        return False


def get_general_option():

    return """\n▶️  what do you want to do❓
    1️⃣ . 🎯  Manage your projects.
    2️⃣ . ✅  Manage your tasks.
    3️⃣ . ❌  Exit()
          """


def get_project_option():
    return """\n▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    3️⃣ . ➕ Add project
    4️⃣ . 🔄 Update project
    5️⃣ . ➖ Delete project
    6️⃣ . 🔙 Back
    7️⃣ . ❌ Exit
    """


def get_task_option():
    return """\n▶️  What do you want to do❓
    1️⃣ . 👁️  Display tasks
    2️⃣ . 👁️  Display a task with id
    3️⃣ . ➕ Add task
    4️⃣ . 🔄 Update task
    5️⃣ . ➖ Delete task
    6️⃣ . 🔙 Back
    7️⃣ . ❌ Exit
    """


def invalid_option() -> str:
    return "⚠️  Invalid option. Please try again. ⚠️"


if __name__ == "__main__":
    main()
