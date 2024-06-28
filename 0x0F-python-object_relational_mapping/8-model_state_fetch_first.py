#!/usr/bin/python3
"""
Script that prints the first State object from the database hbtn_0e_6_usa

Usage: ./8-model_state_fetch_first.py
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
    first_state = session.query(State).order_by(State.id).first()

    if first_state:
        print("{}: {}".format(first_state.id, first_state.name))
    else:
        print("Nothing")

    session.close()
