#!/usr/bin/python3
"""
Script that defines a State class and creates a table in the database.
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

