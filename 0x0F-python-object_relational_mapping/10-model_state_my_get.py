#!/usr/bin/python3
"""
Script that prints the State object with the name passed as argument
    from the database hbtn_0e_6_usa

Usage: ./10-model_state_my_get.py
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

    # Query all State objects and print the passed state
    find_state = session.query(State).order_by(State.id).filter(
        State.name == sys.argv[4]).first()

    if find_state:
        print(find_state.id)
    else:
        print("Not found")

    session.close()
