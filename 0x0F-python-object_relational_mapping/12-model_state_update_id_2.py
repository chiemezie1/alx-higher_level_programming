#!/usr/bin/python3
"""
Script that changes the name of a State object from the database hbtn_0e_6_usa

Usage: ./12-model_state_update_id_2.py
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

    # Change the name of the State where id = 2 to New Mexico
    state = session.query(State).filter(State.id == 2).first()
    state.name = "New Mexico"
    session.commit()
    
    session.close()
