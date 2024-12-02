from .data_type import DataType  # Import parent class DataType

# this file was reformated by black module


class Task(DataType):
    """
    A Task class that extends the DataType parent class, representing a task with a linked project.
    This class provides methods to:
        - Initialize a task with an empty linked project
        - Convert the task data to a dictionary
        - Add a linked project to the task with validation
    Attributes:
        linked_project (str): A list to store tasks associated with the project.
    Inherits from:
        DataType: A parent class providing basic data type functionality.
    """

    def __init__(self):
        super().__init__()
        self.linked_project = ""

    def convert_to_dict(self) -> dict:
        data: dict = DataType.convert_to_dict(self)
        data["linked_project"] = self.linked_project
        return data

    def data_from_dict(self, data: dict) -> None:
        super().data_from_dict(data)
        if self.linked_project:
            """
            this code will not be executed because we choose that linked_project can be only modified by adding the task to a project
            when update task list for a project the id of the project is add to the task
            when a project is deleted the property linked project for all task linked to it are deleted
            """
            print(
                f" This Task is already linked to the project ID= {self.linked_project}"
            )
            answer = (
                input(
                    " Are you sur you want to link it to another project instead?(yes/no): "
                )
                .strip()
                .lower()
            )
            if answer in ["yes", "y"]:
                self.linked_project = data["linked_project"]
                print(f"🟢  Your linked_project has been updated  successfully 🟢")
            else:
                raise ValueError("🔴  The update was canceled 🔴")

        else:
            if "linked_project" in data:
                self.linked_project = data["linked_project"]
