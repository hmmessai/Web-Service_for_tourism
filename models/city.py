#!/usr/bin/python3
"""City Definition"""
import json
from models.basemodel import BaseModel
import models

class City(BaseModel):
    """City Representation"""
    def __init__(self, name=None):
        """Initialization of City instance"""
        super().__init__(name)
