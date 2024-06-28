#!/usr/bin/python3
"""
Script that updates the name of the State where id = 2 to New Mexico
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""Usage: ./12-model_state_update_id_2.py
              <mysql username> <mysql password> <database name>
              """
              )
        sys.exit(1)

    try:
        # Create engine to connect to MySQL database
        engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.format(
            sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)
        print("Database connection established.")

        # Create all tables in the engine
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        # Query the State object with id = 2
        state = session.query(State).filter(State.id == 2).first()

        # Check if state exists
        if state:
            state.name = 'New Mexico'
            session.commit()

            print("State name updated to New Mexico.")
        else:
            print("State with id = 2 not found.")
    except Exception as e:
        print("Error: ", e)
    finally:
        # Close the session
        session.close()
