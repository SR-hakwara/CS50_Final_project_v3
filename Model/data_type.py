# this file was reformated by black module
class DataType:
    """
    This class represents a data type with various descriptive attributes.
    It allows converting its data into a dictionary or to initialize it from a dictionary.
    Attributes:
        id (str): Unique identifier of the object
        name (str): Name of the data type
        description (str): Short description or summary of the object
        detailed_description (str): Detailed description of the object
        creation_date (str): Creation date of the data type (expected format: string)
        deadline (str): Deadline associated with the data type (expected format: string)
        state (str): State or status of the data type.
    """

    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""
        self.detailed_description = ""
        self.creation_date = ""
        self.deadline = ""
        self.state = ""

    def convert_to_dict(self) -> dict:
        """
        Converts the object's attributes into a dictionary.
        Returns :
            dict : Each key in the dictionary corresponds to an attribute of the object.
        """
        data: dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "detailed_description": self.detailed_description,
            "creation_date": self.creation_date,
            "deadline": self.deadline,
            "state": self.state,
        }
        return data

    def data_from_dict(self, data: dict) -> None:
        """
        Updates the object's attributes from a given dictionary.
        The input dictionary must contain all keys corresponding to the class's attributes.
        Args:
            data (dict): input dictionary contains all keys corresponding to the class's attributes.
        """
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.detailed_description = data["detailed_description"]
        self.creation_date = data["creation_date"]
        self.deadline = data["deadline"]
        self.state = data["state"]
