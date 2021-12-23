#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')
    if getenv("HBNB_TYPE_STORAGE") != 'db':

        @property
        def cities(self):
            allcities = []
            for city in models.storage.all('City').values():
                if self.id == city.state_id:
                    allcities.append(city)
            return allcities
