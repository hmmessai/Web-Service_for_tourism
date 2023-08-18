#!/usr/bin/python3
"""File Storage Definition"""
import json
from models.basemodel import BaseModel
from models.city import City


class FileStorage:
    """FileStorage Representation"""

    classes = {'BaseModel': BaseModel, 'City': City}
    __file = 'file.json'
    __objects = {}
    def __init__(self):
        """Initialization of the FileStorage instance"""
        
    def new(self, obj):
        """Adds a newly created object to objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + str(obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves all created instances"""
        dictrep = {}
        for k, v in FileStorage.__objects.items():
            dictrep[k] = str(v)

        with open(FileStorage.__file, 'w') as f:
            json.dump(dictrep, f)

    def reload(self):
        """Reloads existing objects from the file"""
        try:
            with open(FileStorage.__file) as f:
                obj = json.load(f)
                for k, v in obj.items():
                    eval(v.__class__.__name__)()
                    FileStorage.__objects[k] = v
        except Exception:
            pass
