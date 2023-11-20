#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        ''' A Storage file for relationship '''
        @property
        def cities(self):
            '''
            Displays the list of City instances
            with state_id == to the current State.id
            '''
            from models import storage
            from models.city import City

            cityList = []
            cityDict = storage.all(City)

            for city in cityDict.values():
                if city.state_id == self.id:
                    cityList.append(city)
            return cityList
