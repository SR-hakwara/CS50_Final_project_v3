from Model import *
import os
import csv

# this file was reformated by black module
# File paths for projects and tasks databases
PROJECTS_File = "./DB/projects.csv"
TASKS_File = "./DB/tasks.csv"


class Data:
    """
    A generic data management class for handling CSV-based data storage and retrieval.
    This class provides methods to read from and write to CSV files,
    convert data between dictionary and object representations,
    Attributes :
        data_type (str): Type of data being managed (project' or 'task')
        path_file (str): Path to the CSV file
        data (list[dict]): Raw data from CSV file as list of dictionaries
        objects (list[DataType]): list of object converted by self.get_objects() from self.data (project or task)
    """

    def __init__(self, path_file: str, data_type: str):
        """
        Initialize the Data object with file path and data type.
        Args:
            path_file (str): Path to the CSV file
            data_type (str): Type of data being managed
        """
        self.data_type = data_type
        self.path_file = path_file
        self.data: list = []
        self.objects: list = []

    def data_from_csv(self) -> list:
        """
        Read data from CSV file and convert to a list of dictionaries
        and with self.get_objects() to objects.
        Returns:
            list: List of dictionaries containing CSV data
        Raises:
            ValueError: If a file is empty or doesn't exist
        """
        data = []
        if os.path.exists(self.path_file):
            if os.path.getsize(self.path_file):
                with open(self.path_file, "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        data.append(row)
                self.data = data
                self.get_objects()
                return data
            else:
                raise ValueError(
                    f"⚠️  the file for your {self.data_type}s is empty. Choose option 3 to add some ⚠️"
                )
        else:
            raise ValueError(
                f"⚠️  the file for your {self.data_type}s does not exist. Choose option 3 to add some ⚠️"
            )

    def data_to_csv(
        self,
    ) -> None:
        """
        Write data to CSV file.
        Raises:
            ValueError: If no data is present to write
        """
        if not os.path.exists("DB"):
            os.makedirs("./DB")
        with open(self.path_file, "w", newline="") as file:
            if self.data:
                fieldnames = list(self.data[0].keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not os.path.getsize(self.path_file):
                    writer.writeheader()
                for row in self.data:
                    writer.writerow(row)
            else:
                raise ValueError(f"⚠️  they are no data now in your {self.data_type} ⚠️")

    def get_all_ids(self) -> list:
        """
        Get all IDs from the data.
        Convert it to int so we can use it to create new unique id
        Returns:
            list[int]: List of all object IDs
        """
        return [int(data["id"]) for data in self.data]

    def get_object(self, id_: str) -> DataType:
        """
        Retrieve an object from self.objects by its ID.
        Args:
            id_ (str): ID of the object to retrieve
        Returns:
            DataType: Object with the specified ID
        Raises:
            ValueError: If no object with the given ID exists
        """
        for object_ in self.objects:
            if object_.id == id_:
                return object_
        raise ValueError(f"⚠️  No {self.data_type} with this ID ⚠️")

    def get_object_by_property_value(self, property_, value) -> DataType:
        """
        Retrieve an object by a specific property (hasattr) value (getattr).
        Args:
            property_ (str): Name of the property to search
            value (str): Value of the property to match
        Returns:
            DataType: Object with matching property value
        Raises:
            ValueError: If no object with the given property value exists
        """
        for object_ in self.objects:
            if hasattr(object_, property_):
                if value in getattr(object_, property_):
                    return object_
        raise ValueError(f"⚠️  No {self.data_type} with {property_} = {value}⚠️")

    def delete_object(self, object_) -> None:
        """
        Remove an object from the object list.

        Args:
            object_ (DataType): Object to be removed
        """
        self.objects.remove(object_)

    def get_objects(self) -> list:
        """
        Convert dictionary data to objects.
        Put the object in self.objects
        Returns:
            list[DataType]: List of created objects
        """
        all_objects = []
        object_: DataType
        for data_dict in self.data:
            if self.data_type == "project":
                object_ = Project()
            elif self.data_type == "task":
                object_ = Task()
            object_.data_from_dict(data_dict)
            all_objects.append(object_)
        self.objects = all_objects
        return all_objects

    def set_objects(self) -> None:
        """
        Convert objects back to dictionary data.
        """
        self.data = []
        for object_ in self.objects:
            self.data.append(object_.convert_to_dict())

    def get_all_property_value(self, property_) -> list:
        """
        Get all values for a specific property across objects.
        Used for retrieving all used tasks id in project task list
        Args:
            property_ (str): Name of the property to retrieve
        Returns:
            list[str]: List of property values
        """
        values = []
        for object_ in self.objects:
            values.append(getattr(object_, property_))
        return values


class Projects(Data):
    """
    Specialized Data class for managing project-related data.
    Inherits from Data and initializes with a project-specific file path.
    """

    def __init__(self, path_file=PROJECTS_File):
        super().__init__(path_file, "project")


class Tasks(Data):
    """
    Specialized Data class for managing task-related data.
    Inherits from Data and initializes with a task-specific file path.
    """

    def __init__(self, path_file=TASKS_File):
        super().__init__(path_file, "task")
