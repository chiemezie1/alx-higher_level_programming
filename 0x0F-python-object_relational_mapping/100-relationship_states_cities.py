#!/usr/bin/python3
"""
Script that creates the State "California" with the City "San Francisco"
    in the database hbtn_0e_100_usa
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from relationship_state import Base, State
from relationship_city import City

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            """
            Usage: ./100-relationship_states_cities.py
              <mysql username> <mysql password> <database name>
            """
        )
        sys.exit(1)

    # Create engine to connect to MySQL database
    engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)

    # Create all tables in the engine
    Base.metadata.create_all(engine)

    # Bind engine to session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the State "California" with the City "San Francisco"
    new_state = State(name="California")
    new_city = City(name="San Francisco", state=new_state)

    session.add(new_state)
    session.add(new_city)
    session.commit()

    # Close the session
    session.close()
