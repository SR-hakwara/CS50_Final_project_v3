# Project and Task Management Application
#### Video Demo:  <[URL HERE](https://youtu.be/fTGGksKg6LY)>
#### Description: An application for project and task management, which uses the command line to interact with the user
## Overview
This CLI (Command Line Interface) application for project and task management is a simple tool developed in Python.
It allows users to easily manage projects and tasks through a series of basic features,
such as creating, viewing, updating, and deleting projects and tasks (CRUD).
All data is saved in CSV files for easy management and data persistence.
Additionally, modifications to a project or task are reflected in their linked entities.
For instance, deleting a task automatically removes it from the task_list of the associated project,
ensuring that all relationships remain consistent and up to date.

## File Structure
- `project.py`: Main application script managing view and containing some core functionality, and data validation.
- `controller.py`: Controlling data transfert between the view the database (csv files) and model files.
- `test_project`: File for testing the core functionality
- `README.md`: This file.
- `.requirement.txt`: the module and library used in the project.
- `./BD/projects.csv`: CSV file storing project information
- `./BD/tasks.csv`: CSV file storing task information
- `./Model/__init__.py`: to declare the folder as a package and import all model
- `./Model/data_type.py`: Defines a base class with shared attributes and methods for all models.
- `./Model/project_.py`: Represents the project model, inheriting from data_type.
- `./Model/task.py`: Represents the task model, inheriting from data_type.

## Design Choices and Justifications

This project uses CSV files to store data because they're straightforward to use, portable, and easy to edit.
While databases could handle larger systems, they were unnecessary for the size of this project.
SQLite3, which is integrated into Python, could also be used.
It would offer advantages such as better performance with large datasets, more advanced querying capabilities,
and built-in data integrity checks.

The program follows a structure inspired by MVC (Model-View-Controller).
The controller retrieves data from CSV files and converts it into objects using models.
The main file acts as the interface, where users interact with the system.
It also validates inputs before sending them to the controller.

A base class, data_type, was created to avoid duplicating common features like converting objects into dictionaries.
This keeps the code clean and reusable.

Finally, error handling and validation ensure that users can't input incorrect data, like deadlines in the past.
This improves the user experience and prevents issues during operation.

## Libraries Used
- `black` formating all files.
- `mypy` typing hint
- `pytest` for testing.
- `os` to check file state (exist, empty)
- `csv` module for manipulation of csv files for data storage
- `tabulate` library for formatted table display
- `datetime` for date handling
- `re` (regular expressions) for date validation (deadline)
- `literal_eval` from `ast` to safely convert the string representation of a list to an actual list (eval() is more risky)

## Fonctionnalités principales

**selection what we want to manage**
- Manage projects
- Manage tasks
- quit

**Project Management**
- Show all projects
  - The detailed description property is not displayed.
- Show the details of a project using its ID
  - The detailed description property is displayed.
  - Display any tasks linked to the project.
- Add a new project:
  - The ID is generated automatically. If a project is deleted, its ID is reused for the next project creation.
- Update a project:
  - For the "task_list" only a task ID already existing on the task file and not used by another project can be added.
  - When the "task_list" property of a project is modified, the "linked_project" property of the task that was added is automatically updated with the project's ID.
  - When updating "task_lis" if the task ID is already in the project, the task is deleted from the project but with a confirmation message before.
  - The deadline must be today or later and must follow the format YYYY-MM-DD.
- Delete a project.
  - If a project is deleted, the "linked_project" property of any task linked to this project is also deleted.
- Return.
- Quit.

**Task Management**
- Show all tasks
  - the long description property is not displayed.
- Show the details of a task using its ID
  - the detailed description property is displayed.
- Add a new task
    - The ID is generated automatically. If a task is deleted, its ID is reused for the next task creation
    - We can choose to add a linked project or not if we do the task ID is added to the property tak_list of the project add.
    - Only one project can be linked with a task
- Update a task
  - In the "linked_project" property only a project ID already existing on the project file can be added. the task ID is added to the property tak_list of the project add.
  - If a project is already linked with the task, we can't update it, to do so we go to manage a project.
  - The deadline must be today or later and must follow the format YYYY-MM-DD.
- Delete a task
  - If a task is deleted, the task ID is removed from the "task_list" property of any project linked to this task.
- return
- quit


## Usage Example
### Launching the Application
```
python project.py
```
### Project and TaskManagement Workflow
#### 1. Main Menu Navigation
```
★★★  Welcome to CS50 Project ★★★
▶▶  Project and Tasks Management ◀◀

▶️  what do you want to do❓
    1️⃣ . 🎯  Manage your projects.
    2️⃣ . ✅  Manage your tasks.
    3️⃣ . ❌  Exit()
 ```
#### 2. Displaying Projects
```
🔵 Choose an option: 1

▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    3️⃣ . ➕ Add project
    4️⃣ . 🔄 Update project
    5️⃣ . ➖ Delete project
    6️⃣ . 🔙 Back
    7️⃣ . ❌ Exit

🔵 Choose an option: 1
+------+------------------------+-------------------------------+-----------------+-------------+-------------+-------------+
|   id | name                   | description                   | creation_date   | deadline   | state       | task_list   |
+======+========================+===============================+=================+=============+=============+=============+
|    1 | Website Redesign       | Redesign the company website  | 2024-12-01      | 2025-01-15  | In Progress | ['1', '2']  |
+------+------------------------+-------------------------------+-----------------+-------------+-------------+-------------+
|    2 | Mobile App Development | Develop a mobile application  | 2024-12-01      | 2025-02-28  | To do       | ['4', '5']  |
|      |                        | for internal use              |                 |             |             |             |
+------+------------------------+-------------------------------+-----------------+-------------+-------------+-------------+
|    3 | Marketing Campaign     | Plan a marketing campaign for | 2024-12-01      | 2025-03-01  | To do       | []          |
|      |                        | Q1 2025                       |                 |             |             |             |
+------+------------------------+-------------------------------+-----------------+-------------+-------------+-------------+
Press Enter to continue ➡️  ...
```
#### 3. Displaying a single project
```
▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    ...

🔵 Choose an option: 2
➡️  Enter the project id you want to view: 2
+------+------------------------+------------------------------+----------------------------+-----------------+-------------+---------+-------------+
|   id | name                   | description                  | detailed_description       | creation_date   | deadline   | state   | task_list   |
+======+========================+==============================+============================+=================+=============+=========+=============+
|    2 | Mobile App Development | Develop a mobile application | Build an app to streamline | 2024-12-01      | 2025-02-28  | To do   | ['4', '5']  |
|      |                        | for internal use             | employee workflows         |                 |             |         |             |
+------+------------------------+------------------------------+----------------------------+-----------------+-------------+---------+-------------+

Project Tasks:
+------+-------------------+------------------------------+-----------------+-------------+-------------+------------------+
|   id | name              | description                  | creation_date   | deadline   | state       |   linked_project |
+======+===================+==============================+=================+=============+=============+==================+
|    4 | App Wireframes    | Design wireframes for the    | 2024-12-03      | 2024-12-20  | In Progress |                2 |
|      |                   | mobile app                   |                 |             |             |                  |
+------+-------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    5 | Build App Backend | Develop backend APIs for the | 2024-12-10      | 2025-02-20  | To do       |                2 |
|      |                   | mobile app                   |                 |             |             |                  |
+------+-------------------+------------------------------+-----------------+-------------+-------------+------------------+
Press Enter to continue ➡️  ...
```
#### 4. Adding a New Project
```
▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    3️⃣ . ➕ Add project
    ...

🔵 Choose an option: 3
➡️  Enter project name: project test
➡️  Entrer a short description for the project: a short description
➡️  Enter a detailed description for the project: a longer detailed description
➡️  Enter deadline (YYYY-MM-DD ie:2024-12-31): 2024-12-05
🟢 your project has been added successfully with ID = 4 🟢
Press Enter to continue ➡️  ...
```
#### 5. Updating a Project
```
▶️  What do you want to do❓
    ...
    4️⃣ . 🔄 Update project
    ...

🔵 Choose an option: 4
➡️  Enter project ID you want to update: 4
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+
|   id | name         | description         | detailed_description          | creation_date   | deadline   | state   | task_list   |
+======+==============+=====================+===============================+=================+=============+=========+=============+
|    4 | project test | a short description | a longer detailed description | 2024-12-04      | 2024-12-05  | To do   | []          |
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+
🔄  Which Property you want to update ?: task list
📋  list of available task : ['3: Backend Integration', '6: Create Marketing Assets']
➡️  Enter the ID of the task you want to add to this project: 6
🟢  The property 'task_list' has been updated successfully! 🟢

▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    ...

🔵 Choose an option: 2
➡️  Enter the project id you want to view: 4
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+
|   id | name         | description         | detailed_description          | creation_date   | deadline   | state   | task_list   |
+======+==============+=====================+===============================+=================+=============+=========+=============+
|    4 | project test | a short description | a longer detailed description | 2024-12-04      | 2024-12-05  | To do   | ['6']       |
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+

Project Tasks:
+------+-------------------------+-----------------------------+-----------------+-------------+---------+------------------+
|   id | name                    | description                 | creation_date   | deadline   | state   |   linked_project |
+======+=========================+=============================+=================+=============+=========+==================+
|    6 | Create Marketing Assets | Develop marketing materials | 2024-12-05      | 2025-02-15  | To do   |                4 |
|      |                         | for the campaign            |                 |             |         |                  |
+------+-------------------------+-----------------------------+-----------------+-------------+---------+------------------+
Press Enter to continue ➡️  ...
```
#### 6. Deleting a Project
```
▶️  What do you want to do❓
    ...
    5️⃣ . ➖ Delete project
    ...

🔵 Choose an option: 5
➡️  Enter the project ID you want to delete: 4
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+
|   id | name         | description         | detailed_description          | creation_date   | deadline   | state   | task_list   |
+======+==============+=====================+===============================+=================+=============+=========+=============+
|    4 | project test | a short description | a longer detailed description | 2024-12-04      | 2024-12-05  | To do   | ['6']       |
+------+--------------+---------------------+-------------------------------+-----------------+-------------+---------+-------------+
⚠️  Are You sur you want delete this project (yes/no)❓: y
🟢  Your project has been deleted successfully 🟢
```
### Task Management Workflow
for task management, its same use as project management.
#### 1. Switching to Task Management
```
▶️  What do you want to do❓
    1️⃣ . 👁️  Display projects
    2️⃣ . 👁️  Display a project with id
    3️⃣ . ➕ Add project
    4️⃣ . 🔄 Update project
    5️⃣ . ➖ Delete project
    6️⃣ . 🔙 Back
    7️⃣ . ❌ Exit

🔵 Choose an option: 6

▶️  what do you want to do❓
    1️⃣ . 🎯  Manage your projects.
    2️⃣ . ✅  Manage your tasks.
    3️⃣ . ❌  Exit()

🔵 Choose an option: 2

▶️  What do you want to do❓
    1️⃣ . 👁️  Display tasks
    2️⃣ . 👁️  Display a task with id
    3️⃣ . ➕ Add task
    ...

🔵 Choose an option: 1
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|   id | name                    | description                  | creation_date   | deadline   | state       | linked_project   |
+======+=========================+==============================+=================+=============+=============+==================+
|    1 | Create Wireframes       | Design wireframes for the    | 2024-12-02      | 2024-12-15  | Completed   | 1                |
|      |                         | website redesign             |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    2 | Develop Frontend        | Implement frontend for the   | 2024-12-05      | 2025-01-10  | In Progress | 1                |
|      |                         | website                      |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    3 | Backend Integration     | Connect the backend to the   | 2024-12-08      | 2025-01-15  | To do       |                  |
|      |                         | frontend                     |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    4 | App Wireframes          | Design wireframes for the    | 2024-12-03      | 2024-12-20  | In Progress |                  |
|      |                         | mobile app                   |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    5 | Build App Backend       | Develop backend APIs for the | 2024-12-10      | 2025-02-20  | To do       | 2                |
|      |                         | mobile app                   |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
|    6 | Create Marketing Assets | Develop marketing materials  | 2024-12-05      | 2025-02-15  | To do       |                  |
|      |                         | for the campaign             |                 |             |             |                  |
+------+-------------------------+------------------------------+-----------------+-------------+-------------+------------------+
Press Enter to continue ➡️  ...
```
### Exiting the Application
```
Choose an option: 3  # Exit from main menu

👋👋 Goodbye! See you soon !!🙂

```
```
(CTRL+D )

👋👋 Goodbye! See you soon !!🙂

```
### Error message
#### Deadline error
Deadline must be in the future and in the format YYYY-MM-DD.
```
➡️  Enter deadline (YYYY-MM-DD ie:2024-12-31): 2024-12-03  # Eralier date than today
⚠️ Deadline must be today or later, and in the format (YYYY-MM-DD, e.g., 2025-01-30) ⚠️
➡️  Enter deadline (YYYY-MM-DD ie:2024-12-31): 2025-31-12  # Wrong format YYYY-DD-MM
⚠️ Deadline must be today or later, and in the format (YYYY-MM-DD, e.g., 2025-01-30) ⚠️
```
#### File error
```
🔵 Choose an option: 1
⚠️  The file for your projects does not exist. Choose option 3 to add some ⚠️
```
```
🔵 Choose an option: 1
⚠️  The file for your projects is empty. Choose option 3 to add some ⚠️
```
#### Task_list update error
We can only choose a task ID in a list of available task
```
🔄  Which Property you want to update ?: task lists
🔴  The property 'task_lists' does not exist in the project 🔴
🔄  Which Property you want to update ?: task list
📋  list of available task : ['3: Backend Integration', '4: App Wireframes']
➡️  Enter the ID of the task you want to add to this project: 1
⚠️ This task is already used in other project ⚠️
📋  list of available task : ['3: Backend Integration', '4: App Wireframes']
➡️  Enter the ID of the task you want to add to this project: 7
⚠️  No task with this ID ⚠️
📋  list of available task : ['3: Backend Integration', '4: App Wireframes']
➡️  Enter the ID of the task you want to add to this project: 3
🟢  The property 'task_list' has been updated successfully! 🟢
```
#### Three wrong attempts
we have three attempts if we enter the wrong data for deadline, task_list and linked_project properties.
```
⚠️ 3 wrong attempt start again ⚠️
```

## Conclusion

This project represents a practical and functional application for managing projects and tasks.
By combining Python's object-oriented programming with an MVC-inspired structure,
the program achieves a balance between simplicity and extensibility.
Previous versions of this program, which did not follow the MVC model,
can still be found in the folder ./old_versions/. They reflect the iterations and attempts I made before reaching this final version.

The use of CSV files for data persistence makes the system lightweight and accessible,
while robust validation and error-handling ensure data integrity.
The application's modular design also lays the foundation for future improvements,
such as integrating a database or transitioning to a graphical interface.

Thank you for exploring this project,
which demonstrates the core principles of software development and highlights key aspects of the CS50 introduction to programming with python course.
