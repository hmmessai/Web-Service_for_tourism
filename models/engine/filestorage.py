#!/usr/bin/python3
"""File Storage Definition"""
import json
import re
from operator import itemgetter
from models.basemodel import BaseModel
from models.city import City
from models.place import Place
from models.user import User

classes = {
    'BaseModel': BaseModel,
    'City': City,
    'Place': Place,
    'User': User
    }

class FileStorage:
    """FileStorage Representation"""

    __objects = {}


    def __init__(self, file_path=None):
        """Initializes the file storage"""
        if file_path is None:
            self.__file = 'storage/file.json'
        else:
            self.__file = file_path

    def all(self, cls=None):
        """Reterives all objects of the given class"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects


    def new(self, obj):
        """Adds a newly created object to objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + str(obj.id)
            self.__objects[key] = obj

    def rollback(self):
        """Rollback the file storage"""
        with open(self.__file, 'r+') as f:
            f.seek(0, 2)
            f.write("\"\" }}")
        with open(self.__file, 'r+') as f:
            obj = json.load(f)
            f.seek(0)
            f.truncate()
            dic = {}
            print(obj)
            for index,(key, value) in enumerate(obj.items()):
                if index < len(obj):
                    dic[key] = value
            print(dic)
            json.dump(dic, f)

    def search(self, cls, keyword):
        """Searchs for a keyword for a specific class"""
        results = []
        if cls is not None:
            names = []
            vals = self.all(cls)
            for value in vals.values():
                names.append(value.name)
            keyword = f'^{re.escape(keyword.lower()[:-1])}.*'
            for name in names:
                if re.search(keyword, name.lower(), re.IGNORECASE):
                    for value in vals.values():
                        if value.name == name:
                            results.append(value)
            return results
        return results


                

    def save(self):
        """Saves all created instances"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file, 'w') as f:
            json.dump(json_objects, f)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]


    def reload(self):
        """Reloads existing objects from the file"""
        try:
            with open(self.__file) as f:
                obj = json.load(f)
                for k, v in obj.items():
                    restored_obj = eval(v['__class__'])(**v)
                    self.new(restored_obj)
        except FileNotFoundError:  # Handle the case where the file doesn't exist
            with open(self.__file, 'w') as f:  # Create an empty file
                pass
        except Exception as e:
            print(e)
