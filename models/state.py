#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.city import City
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    if models.engineMode == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')

    else:
        name = ""

        @property
        def cities(self):
            allcities = []
            for city in models.storage.all(City).values():
                if self.id == city.state_id:
                    allcities.append(city)
            return allcities
