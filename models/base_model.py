#!/usr/bin/python3

from datetime import datetime
import uuid
from models import storage


class BaseModel:
    """Class from which all other classes will inherit"""

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """
        if kwargs and kwargs != {}:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(
                        self,
                        key,
                        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"),
                    )
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns official string representation"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """updates the public instance attribute updated_at"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict

