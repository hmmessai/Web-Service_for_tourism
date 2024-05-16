#!/usr/bin/python3
"""Place Definition"""
import models
from models.basemodel import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey, Text

class Place(BaseModel, Base):
    """Place Representation"""

    __tablename__ = 'places'
    name = Column(String(128), nullable=False)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    type = Column(String(100), nullable=False)
    price = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)

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