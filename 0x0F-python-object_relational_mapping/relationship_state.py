#!/usr/bin/python3
"""
Script that defines a State class and creates a table in the database.
If the State object is deleted,
    all linked City objects must be automatically deleted.

"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class State(Base):
    """
    State class that inherits from Base
    - Links to the MySQL table 'states'
    - Has id and name attributes
    """
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(128), nullable=False)
    cities = relationship(
        'City', backref='state', cascade='all, delete-orphan'
    )
