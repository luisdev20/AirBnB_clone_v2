#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, Column, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table, PrimaryKeyConstraint


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False),
                      PrimaryKeyConstraint('place_id', 'amenity_id'))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place",
                           cascade="all, delete-orphan")
    amenity_ids = []
    amenities = relationship("Amenity", secondary=place_amenity,
                             back_populates="place_amenities",
                             viewonly=False)

    if models.engineMode != "db":

        @property
        def amenities(self):
            amen_plc = []
            allAmenities = models.storage.all('Amenity').values()
            for am in allAmenities:
                if am.id in Place.amenity_ids:
                    amen_plc.append(am)
            return amen_plc

        @amenities.setter
        def amenities(self, value):
            if type(value) is Amenity:
                Place.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Return a list of Review instances with Place_id"""
            list_reviews = []
            for review in list(models.storage.all('Review').values()):
                if review.place_id == self.id:
                    list_reviews.append(review)
            return list_reviews
