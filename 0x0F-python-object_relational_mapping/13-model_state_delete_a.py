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

        # Query  and delete all objects that contain letter 'a' in their name
        states_to_delete = session.query(State).filter(
            State.name.like('%a%')
            ).all()

        for state in states_to_delete:
            session.delete(state)

        # Commit the changes
        session.commit()
        print("Deletion completed.")

    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    finally:
        # Close the session
        if session is not None:
            session.close()
            print("Session closed.")
