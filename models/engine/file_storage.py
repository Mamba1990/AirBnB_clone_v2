#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """This class manages storage of hbnb models in JSON format
    Attributes:
        __file_path: The JSON's file path.
        __objects: A dictionary that will store instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        Return:
            returns a dictionary that will store instances
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for k in dictionary:
                partition = k.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[k] = self.__objects[k]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary
        Args:
            obj: The given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deleting an existing element
        """
        if obj:
            k = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[k]

    def close(self):
        """ Makes call to reload()
        """
        self.reload()
