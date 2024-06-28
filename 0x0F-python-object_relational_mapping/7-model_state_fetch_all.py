#!/usr/bin/python3
"""
Script that lists all State objects from the database hbtn_0e_6_usa

Usage: ./7-model_state_fetch_all.py
    <mysql username> <mysql password> <database name>
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

    # Query all State objects and print them
    for state in session.query(State).order_by(State.id).all():
        print("{}: {}".format(state.id, state.name))

    session.close()
