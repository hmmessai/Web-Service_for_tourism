#!/usr/bin/python3
"""City Definition"""
import models
from models.basemodel import BaseModel

class City(BaseModel):
    """City Representation"""
    def __init__(self, *args, **kwargs):
        """Initialization of City instance"""
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'name') or not self.name:
            self.name = 'Addis Ababa'
        


    @classmethod
    def search(cls, name):
        """Searches city by name"""
        cities = models.storage.all(City)
        for city in cities.values():
            if city.name == name:
                return city

        return None, "**Cannot find city with name: " + name + "***"
    
    @classmethod
    def places(cls, name):
        all_places = models.storage.all(models.place.Place)
        list_of_places = []
        for place in all_places.values():
            if place.city and place.city == name:
                list_of_places.append(place)
        
        return list_of_places

