#!/usr/bin/python3
"""
Script that deletes all State objects with a name containing the letter a
    from the database hbtn_0e_6_usa
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_state import Base, State


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            """
            Usage: ./13-model_state_delete_a.py
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

        # Query all State objects and delete the ones with the letter a
        for state in session.query(State).filter(State.name.like('%a%')):
            session.delete(state)

        # Commit the changes
        session.commit()

        # Close the session
    except Exception as e:
        print("Error: ", e)
    finally:
        # Close the session
        session.close()
