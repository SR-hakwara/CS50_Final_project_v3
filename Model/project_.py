from .data_type import DataType  # Import parent class DataType
import ast  # Import ast to convert a string to a list

# this file was reformated by black module


class Project(DataType):
    """
    A Project class that extends the DataType parent class, representing a project with a list of tasks.
    This class provides methods to:
        - Initialize a project with an empty task list
        - Convert the project data to a dictionary
        - Add tasks to the project with validation
    Attributes:
        task_list (list): A list to store tasks associated with the project
    Inherited from:
        DataType: A parent class providing basic data type functionality
    """

    def __init__(self):
        super().__init__()
        self.task_list = list()

    def convert_to_dict(self) -> dict:
        """
        Convert the project data to a dictionary.
        Returns:
            dict: A dictionary representation of the project,
                  including all parent class data and the task list
        """
        # Get the dictionary from the parent class
        data = DataType.convert_to_dict(self)
        # Add the task list to the dictionary
        data["task_list"] = self.task_list
        return data

    def data_from_dict(self, data: dict) -> None:
        """
        Populate the project data from a dictionary.
        Args:
            data (dict): A dictionary containing project data
        Raises:
            ValueError: If the task being added is already in the project's task list
        """
        super().data_from_dict(data)
        if (
            data["task_list"] in self.task_list and self.task_list
        ):  # if self task list not empty and contain already de new value
            raise ValueError(
                f"🔴 The Task is already linked to this project. task list = {self.task_list} 🔴"
            )
        else:
            # Use ast.literal_eval to safely convert the string representation of a list to an actual list
            self.task_list += ast.literal_eval(data["task_list"])
