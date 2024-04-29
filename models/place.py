#!/usr/bin/python3
"""Place Definition"""
import models
from models.basemodel import BaseModel
from models.city import City

class Place(BaseModel):
    """Place Representation"""
    description = ""
    name = ""


    def __init__(self, *args, **kwargs):
        """Initialiization of TourPlace instance"""
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'name') or not self.name:
            self.name = "New Place"

    @classmethod
    def search(cls, name):
        """Searches city by name"""
        cities = models.storage.all(City)
        for city in cities.values():
            if city.name == name:
                return city

        return None, "**Cannot find city with name: " + name + "***"