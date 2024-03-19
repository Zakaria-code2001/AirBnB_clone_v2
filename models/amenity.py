from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv

class Amenity(BaseModel, Base):
    """
    Amenity inherits from BaseModel and Base
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True),
                              Column('place_id', String(60), ForeignKey('places.id'), primary_key=True))
        
        places = relationship('Place', secondary='place_amenity', back_populates='amenities')
