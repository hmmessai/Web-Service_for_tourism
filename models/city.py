#!/usr/bin/python3
"""City Definition"""
import models
import os
from dotenv import load_dotenv
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

load_dotenv()

DB_STORAGE = os.getenv('DB_STORAGE')

class City(BaseModel, Base):
    """City Representation"""

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    population = Column(Integer, nullable=False)
    region = Column(String(90), nullable=False)
    weather = Column(String(90), nullable=False)
    features = Column(String(90), nullable=True)


    if DB_STORAGE == 'db':
        places = relationship('Place', cascade='all, delete-orphan')
    

    def __init__(self, *args, **kwargs):
        """Initialization of City instance"""
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'name') or not self.name:
            self.name = 'Addis Ababa'
        


    @classmethod
    def search(cls, name):
        """Searches city by name"""
        cities = models.storage.all()
        for city in cities.values():
            if city.name == name:
                return city

        return None, "**Cannot find city with name: " + name + "***"
    
    if DB_STORAGE != 'db':
        @property
        def places(self):
            all_places = models.storage.all(models.place.Place)
            list_of_places = []
            for place in all_places.values():
                if place.city and place.city == self.name:
                    list_of_places.append(place)
            
            return list_of_places

