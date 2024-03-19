from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float, MetaData
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    metadata = MetaData()

    # Check if table already exists
    if 'place_amenity' not in metadata.tables:
        # Define the association table
        place_amenity = Table('place_amenity', metadata,
                              Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
                              Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True))

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary='place_amenity', backref='places', viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter attribute in case of file storage"""
            return [review for review in models.storage.all(Review) if review.place_id == self.id]

        @property
        def amenities(self):
            """Getter attribute in case of file storage"""
            return [amenity for amenity in models.storage.all(Amenity) if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter method for amenities"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
