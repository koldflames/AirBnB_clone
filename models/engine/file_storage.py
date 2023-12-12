#!/usr/bin/python3
"""This defines the module for FileStorage class"""
import datetime
import json
import os
from models.base_model import BaseModel
from models import storage


class FileStorage:
    """Handles serialization and deserialization of objects"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects"""
        return storage.all()

    def new(self, obj):
        """Adds a new object to the dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        storage.all()[key] = obj

    def save(self):
        """Saves objects to a JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in storage.all().items()}
            json.dump(d, f)

    def classes(self):
        """Returns available classes"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return storage.classes()

    def reload(self):
        """Reloads objects from the JSON file"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {k: self.classes()[v["__class__"]](**v) 
                    for k, v in obj_dict.items()}
            FileStorage.__objects = obj_dict

    def attributes(self):
        """Returns attributes for classes"""
        return storage.attributes()

