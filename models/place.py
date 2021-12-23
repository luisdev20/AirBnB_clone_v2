#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import ForeignKey, Column, String, Integer, Float
from models.review import Review
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenity_ids = []

    if models.engineMode != "db":
        @property
        def reviews(self):
            """Return a list of Review instances with Place_id"""
            list_reviews = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    list_reviews.append(review)
            return list_reviews
