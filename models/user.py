#!/usr/bin/python3
"""User Definition"""
import models
from models.basemodel import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey, Text

class User(BaseModel, Base):
    """User Representation"""

    __tablename__ = 'users'
    name = Column(String(128), nullable=False, unique=True)
    city_id = Column(String(60), nullable=False)
    phone_number = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    about = Column(Text, nullable=True)
    password = Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialiization of TourPlace instance"""
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'name') or not self.name:
            self.name = "Anonymous" + self.id

    @classmethod
    def search(cls, name):
        """Searches city by name"""
        cities = models.storage.all('User')
        print(cities)
        for city in cities.values():
            if city.name == name:
                return city

        return None