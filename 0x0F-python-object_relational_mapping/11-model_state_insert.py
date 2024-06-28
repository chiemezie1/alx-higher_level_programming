#!/usr/bin/python3
"""
Script that adds the State object “Louisiana” to the database hbtn_0e_6_usa

Usage: ./11-model_state_insert.py
    <mysql username> <mysql password> <database name> <state name>
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State

if __name__ == "__main__":
    """
    Create engine to connect to MySQL database
    """
    engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)

    Base.metadata.create_all(engine)

    # Bind engine to session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a new State object
    new_state = State(name="Louisiana")
    session.add(new_state)
    session.commit()

    # Print the ID of the new state
    print(new_state.id)

    session.close()