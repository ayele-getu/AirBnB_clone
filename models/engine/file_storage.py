#!/usr/bin/python3
"""Contain the class FileStorage"""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
import json


class FileStorage():
    """ FileStorage Class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects from dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Set in __objects with key <obj class name>.id"""
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def reload(self):
        """deserialization the JSON file to __objects, only JS"""
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as f:
                all_objs = json.loads(f.read())
            for obj_id, obj in all_objs.items():
                name_class = obj_id.split(".")[0]
                self.new(eval(name_class + "(**obj)"))
        except:
            pass

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, mode='w', encoding='utf-8') as f:
            obj_dict = {key_obj: obj.to_dict()
                        for key_obj, obj in self.__objects.items()}
            json.dump(obj_dict, f)
