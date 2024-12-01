import pytest

from project import *
from controller import Projects, Tasks

# this file was reformated by black module
PROJECT_CSV = "temp_projects.csv"
TASK_CSV = "temp_tasks.csv"


def simulate_input(monkeypatch, inputs):
    """
    Simulate user inputs by creating an input generator.
    Args:
        monkeypatch: pytest fixture to simulating system behavior
        inputs: List of simulated user inputs
    """
    input_generator = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_generator))


def clean_csv_files():
    """
    function to ensure clean CSV files after each test.
    """
    # Paths to CSV files

    # Remove existing CSV files if they exist
    if os.path.exists(PROJECT_CSV):
        os.remove(PROJECT_CSV)
    if os.path.exists(TASK_CSV):
        os.remove(TASK_CSV)


def test_project_add(monkeypatch):
    """
    Test adding a new project.
    """
    # Simulate user inputs for project details
    inputs = [
        "Test Project",  # name
        "A test project description",  # description
        "Detailed test project description",  # detailed description
        "2025-12-31",  # deadline
    ]

    # Simulate inputs
    simulate_input(monkeypatch, inputs)

    # Create Projects instance
    project_list = Projects(PROJECT_CSV)

    # Add project
    add_data(project_list)

    # Verify project was added
    project_list.data_from_csv()
    assert len(project_list.data) == 1

    # Check project details
    added_project = project_list.data[0]
    assert added_project["name"] == "Test Project"
    assert added_project["description"] == "A test project description"
    assert added_project["state"] == "To do"
    assert added_project["dead_line"] == "2025-12-31"
    clean_csv_files()


def test_project_update(monkeypatch):
    """
    Test updating an existing project.
    """
    # First, add a project
    project_list = Projects(PROJECT_CSV)
    task_list = Tasks(TASK_CSV)

    # Simulate inputs to add a project
    add_inputs = [
        "Test Project",  # name
        "A test project description",  # description
        "Detailed test project description",  # detailed description
        "2025-12-31",  # deadline
    ]
    simulate_input(monkeypatch, add_inputs)
    add_data(project_list)

    # Simulate inputs for update
    update_inputs = [
        "1",  # project ID to update
        "name",  # property to update
        "Updated Project Name",  # new value
    ]
    simulate_input(monkeypatch, update_inputs)

    # Perform update
    update_data(project_list, task_list)

    # Verify update
    project_list.data_from_csv()
    updated_project = project_list.data[0]
    assert updated_project["name"] == "Updated Project Name"
    clean_csv_files()


def test_project_delete(monkeypatch):
    """
    Test deleting an existing project.
    """
    # First, add a project
    project_list = Projects(PROJECT_CSV)
    task_list = Tasks(TASK_CSV)

    # Simulate inputs to add a project
    add_inputs = [
        "Test Project",  # name
        "A test project description",  # description
        "Detailed test project description",  # detailed description
        "2025-12-31",  # deadline
    ]
    simulate_input(monkeypatch, add_inputs)
    add_data(project_list)
    project_list.data_to_csv()

    # Simulate inputs for deletion (yes to confirm)
    delete_inputs = ["1", "yes"]  # project ID to delete  # confirm deletion
    simulate_input(monkeypatch, delete_inputs)

    # Perform delete
    delete_data(project_list, task_list)

    # Verify deletion. the project file mus be empty, and trying to import data from it raise ValueError
    with pytest.raises(
        ValueError,
        match="⚠️ the file for your projects is empty. Choose option 3 to add some ⚠️",
    ):
        project_list.data_from_csv()
    assert len(project_list.data) == 0
    clean_csv_files()


def test_view_all():
    """
    Test viewing all projects.
    """
    # Create and add multiple projects
    project_list = Projects(PROJECT_CSV)

    # Manually add some projects to test view
    project_list.data = [
        {
            "id": "1",
            "name": "Project 1",
            "description": "First test project",
            "detailed_description": "Detailed description of first project",
            "creation_date": date.today(),
            "dead_line": "2025-12-31",
            "state": "To do",
            "task_list": [],
        },
        {
            "id": "2",
            "name": "Project 2",
            "description": "Second test project",
            "detailed_description": "Detailed description of second project",
            "creation_date": date.today(),
            "dead_line": "2026-01-15",
            "state": "To do",
            "task_list": [],
        },
    ]

    # Save to CSV
    project_list.data_to_csv()

    # View all projects
    result = view_all(project_list)

    # Verify result contains project details
    assert "Project 1" in result
    assert "Project 2" in result
    # in view all we don't display the property detailed_description and its value
    assert "detailed_description" not in result
    # make sur that all data are correctly display with tabulate()
    projects = []
    for project in project_list.data:
        project.pop("detailed_description")
        projects.append(project)

    assert view_all(project_list) == tabulate(
        projects, headers="keys", tablefmt="grid", maxcolwidths=30
    )
    clean_csv_files()


def test_view_single_project(monkeypatch):
    """
    Test viewing a single project by ID.
    """
    # Create and add a project
    project_list = Projects(PROJECT_CSV)

    # Manually add a project to test view
    project_list.data = [
        {
            "id": "1",
            "name": "Test Project",
            "description": "A test project",
            "detailed_description": "Detailed description of test project",
            "creation_date": date.today(),
            "dead_line": "2025-12-31",
            "state": "To do",
            "task_list": [],
        }
    ]
    project_list.data_to_csv()

    # Simulate selecting project ID
    simulate_input(monkeypatch, ["1"])

    # View single project
    result = view_single_data(project_list)

    # Verify result contains project details
    assert "Test Project" in result
    assert "2025-12-31" in result
    # Verify result contains detailed_description in view_single_project unlike view_all function
    assert "detailed_description" in result
    # make sur that all data are correctly display with tabulate()
    simulate_input(monkeypatch, ["1"])
    assert view_single_data(project_list) == tabulate(
        project_list.data, headers="keys", tablefmt="grid", maxcolwidths=30
    )

    clean_csv_files()
