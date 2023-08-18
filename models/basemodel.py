#!/usr/bin/python3
"""BaseModel Definition"""
import datetime
import models
from uuid import uuid4


class BaseModel:
    """BaseModel Representation"""
    def __init__(self, name=None):
        """Initialization of BaseModel instance"""
        self.id = uuid4()
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.name = name
        models.storage.new(self)


    def save(self):
        """Saves the obj to the file storage"""
        models.storage.save()
