#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import environ
from models.amenity import Amenity


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship("Review",
                               backref='place',
                               cascade="all, delete")
        amenities = relationship('Amenity',
                                 backref='place_amenities',
                                 secondary='place_amenity',
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """Returns the list of Review instances
               with place_id equals to the current Place.id"""
            from models import storage
            extracted_reviews = models.storage.all(Review).values()
            review_list = [
                review for review in extracted_reviews
                if review.place_id == self.id
            ]
            return review_list

        @property
        def amenities(self):
            """Returns the list of Amenity instances"""
            from models import storage
            extracted_amenities = models.storage.all('Amenity')
            amenities_list = [
                value for key, value in extracted_amenities.items()
                if key in self.amenity_ids
            ]
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """Append method" that adds an Amenity.id
               to the attribute amenity_ids"""
            if type(obj) == Amenity:
                self.amenity_ids.append('Amenity' + '.' + obj.id)
