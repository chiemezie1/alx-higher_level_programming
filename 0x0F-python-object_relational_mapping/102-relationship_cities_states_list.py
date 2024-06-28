#!/usr/bin/python3
"""
Script that lists all City objects from the database hbtn_0e_101_usa
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
            Usage: ./102-relationship_cities_states_list.py
              <mysql username> <mysql password> <database name>
            """
        )
        sys.exit(1)

    # Create engine to connect to MySQL database
    engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.format(
        sys.argv[1], sys.argv[2], sys.argv[3]), pool_pre_ping=True)

    # Bind engine to session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query all City objects ordered by their id
    cities = session.query(City).order_by(City.id).all()

    # Display the results
    for city in cities:
        print("{}: {} -> {}".format(city.id, city.name, city.state.name))

    # Close the session
    session.close()
