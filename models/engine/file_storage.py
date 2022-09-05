#!/usr/bin/python3
import json
import os


class FileStorage:
    """ Class FileStorage """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return Objects """
        return (FileStorage.__objects)

    def new(self, obj):
        """ Create New Object """
        FileStorage.__objects["{}.{}".format(
            obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """ Save File Json """
        with open(FileStorage.__file_path, 'w') as file_json:
            res = {}
            for key, value in FileStorage.__objects.items():
                res[key] = value.to_dict()
            file_json.write(json.dumps(res))

    def reload(self):
        """ Reload File Json """
        try:    
            with open(FileStorage.__file_path, 'r', encoding="utf-8") as file_json:
                from models.base_model import BaseModel
                from models.user import User
                from models.place import Place
                from models.state import State
                from models.city import City
                from models.amenity import Amenity
                from models.review import Review
                json_des = json.load(file_json)
            for key, value in json_des.items():
                value = eval(value["__class__"])(**value)
                FileStorage.__objects[key] = value
        except OSError:
            pass
