# Project and Task Management Application
#### Video Demo:  <URL HERE> [URL TO ADD]
#### Description: An application for project and task management, which uses the command line to interact with the user
## Overview
This CLI (Command Line Interface) application for project and task management is a simple tool developed in Python.
It allows users to easily manage projects and tasks through a series of basic features, such as creating, viewing, updating, and deleting projects and tasks.
All data is saved in CSV files for easy management and data persistence. Additionally, modifications to a project or task are reflected in their linked entities.
For instance, deleting a task automatically removes it from the task_list of the associated project, ensuring that all relationships remain consistent and up-to-date.

---
## Functionalities and Features
### Core Features

#### Modular Architecture
- Organized into three layers:
  - **Models**: Handles data representation and manipulation.
  - **Controllers**: Manages interactions between the user interface and the model layer.
  - **Interface**: The `project.py` file provides a user-friendly, menu-driven interface.
- Ensures a clear separation of concerns, enhancing scalability and maintainability.

#### Robust Error Handling
- Validates input formats for dates (`YYYY-MM-DD`) and IDs.
- Prevents inconsistencies, such as duplicate task assignments or invalid updates.
- Provides detailed feedback and error messages for invalid inputs or operations.

#### User-Friendly Interface
- Menu-driven navigation ensures accessibility for both technical and non-technical users.
- Logical flow and clear instructions guide users through operations.

---
### Key Functionalities

#### Selection Menu
- **Manage Projects**: Access all features related to project management.
- **Manage Tasks**: Navigate and control all task-related operations.
- **Quit**: Exit the application gracefully.

#### Project Management
- **Show All Projects**:
  - Displays all projects in a tabular format, excluding the long description property.
- **View Project Details**:
  - Displays detailed information about a project, including the long description property and all linked tasks (if any).
- **Add a New Project**:
  - Automatically generates a unique ID for the project. Deleted project IDs are reused for new creations.
  - Includes fields for name, descriptions, and a deadline, which must follow the `YYYY-MM-DD` format and can't be in the past.
- **Update a Project**:
  - Allows updates to any property except the ID.
  - For the `task_list` property:
    - Only existing task IDs can be added.
    - If a task is added, the task's `linked_project` property is automatically updated.
    - If a task already in the list is re-selected, it is removed after user confirmation.
- **Delete a Project**:
  - Removes the project and clears the `linked_project` property of any associated tasks.
- **Return to Menu or Quit**:
  - Navigate back to the main menu or exit the application.

#### Task Management
- **Show All Tasks**:
  - Displays all tasks in a tabular format, excluding the long description.
- **View Task Details**:
  - Shows full details of a task, including the long description and linked project (if any).
- **Add a New Task**:
  - Automatically generates a unique ID for the task. Deleted task IDs are reused for new creations.
- **Update a Task**:
  - Allows modification of task properties except the ID and linked_project
- **Delete a Task**:
  - Removes the task and, if linked to a project, updates the project to reflect the removal.
- **Return to Menu or Quit**:
  - Navigate back to the main menu or exit the application.

---
### Files Overview:
#### **Primary Files**
- **`project.py`**:
  - The main application interface containing high-level control logic and menu navigation.
  - Serves as the entry point for users and integrates models and controllers.

- **`README.md`**:
  - Documentation file describing the project's purpose, architecture, and functionality.

- **`test_project.py`**:
  - Contains test cases for validating the functionality of the system. Ensures robustness and reliability.

- **`requirements.txt`**:
  - Lists all Python dependencies required for running the project.

#### **Controller Layer**
- **`controller.py`**:
  - Manages the interaction between the user interface (`project.py`) and the model layer.
  - Handles operations such as fetching, updating, and saving data.

#### **Model Layer**
- **`model/__init__.py`**:
  - Initializes the model package for importing submodules.

- **`model/data_type.py`**:
  - Defines base data structures and common utilities used across models.

- **`model/project_.py`**:
  - Implements the `Project` class, representing project entities and their attributes.

- **`model/task.py`**:
  - Implements the `Task` class, representing task entities and their relationships with projects.
#### **database file**
- **`DB/projects.csv`**: Stores project data, including details like name, description, creation date, deadline, and linked tasks.

- **`DB/tasks.csv`**: Stores task data, including task names, descriptions, deadlines, and linked projects.

---

### Design Choices:
1. **MVC-inspired Structure**:
   - Maintains a separation between data, control logic, and interface to enhance scalability and maintainability.
   - some of the Control functions are kept in `project.py` for testing purposes as per requirements for CS50 final project.

2. **Object-Oriented Models**:
   - Projects and tasks are encapsulated in classes, ensuring a clear representation of data and behaviors.

3. **CSV for Storage**:
   - Chosen for simplicity and portability. Though less robust than databases, it allows easy inspection and modification of data files.

4. **Scalability**:
   - The modular design facilitates future extensions, such as integrating a database or a graphical user interface.

---

I'll format this for Markdown (.md) to ensure it's displayed correctly:


# CS50 Project Management System

### Run the application 
```
...\project> python project.py
```
### Initial Menu
```
★★★  Welcome to CS50 Poject ★★★
▶▶  Project and Tasks Management ◀◀

▶️  what do you want to do❓
    1️⃣ . 🎯 Manage your projects.
    2️⃣ . ✅ Manage your tasks.
    3️⃣ . ❌ Exit()
          
🔵 Choose an option: 1
```
### Project Management Submenu
```
▶️  What do you want to do❓
    1️⃣ . 👁️ Display projects
    2️⃣ . 👁️ Display a project with id
    3️⃣ . ➕ Add project
    4️⃣ . 🔄 Update project
    5️⃣ . ➖ Delete project
    6️⃣ . 🔙 Back
    7️⃣ . ❌ Exit
```
### View all projects

```
🔵 Choose an option: 1
+------+--------------+-------------------+-----------------+-------------+---------+-------------+
|   id | name         | description       | creation_date   | dead_line   | state   | task_list   |
+======+==============+===================+=================+=============+=========+=============+
|    1 | project test | short description | 2024-12-01      | 2025-01-01  | To do   | ['1']       |
+------+--------------+-------------------+-----------------+-------------+---------+-------------+
|    2 | p2           | sd                | 2024-12-01      | 2025-01-01  | To do   | []          |
+------+--------------+-------------------+-----------------+-------------+---------+-------------+
|    3 | p3           | p3 desc           | 2024-12-01      | 2025-01-01  | To do   | ['2']       |
+------+--------------+-------------------+-----------------+-------------+---------+-------------+
Press Enter to continue ➡️  ...
```
### view a single project
```
🔵 Choose an option: 2
➡️  Enter the project id you want to view: 1
+------+--------------+-------------------+-----------------------------+-----------------+-------------+---------+-------------+
|   id | name         | description       | detailed_description        | creation_date   | dead_line   | state   | task_list   |
+======+==============+===================+=============================+=================+=============+=========+=============+
|    1 | project test | short description | longer detailed description | 2024-12-01      | 2025-01-01  | To do   | ['1']       |
+------+--------------+-------------------+-----------------------------+-----------------+-------------+---------+-------------+

Project Tasks:
+------+-----------+-------------------+-----------------+-------------+---------+------------------+
|   id | name      | description       | creation_date   | dead_line   | state   |   linked_project |
+======+===========+===================+=================+=============+=========+==================+
|    1 | tash test | short description | 2024-12-01      | 2025-01-01  | To do   |                1 |
+------+-----------+-------------------+-----------------+-------------+---------+------------------+
```



