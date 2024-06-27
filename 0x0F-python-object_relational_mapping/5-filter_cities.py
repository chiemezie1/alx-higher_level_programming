#!/usr/bin/python3
"""
Script that takes in the name of a state as an argument
    and lists all cities of that state,
    using the database hbtn_0e_4_usa

Usage: ./5-filter_cities.py
    <mysql username> <mysql password> <database name> <state name>
"""
import sys
import MySQLdb


def list_cities_by_state(username, password, database, state_name):
    """
    Connects to MySQL server and retrieves all cities from 'cities' table
    where state name matches the argument.

    Args:
    - username (str): MySQL username
    - password (str): MySQL password
    - database (str): Database name
    - state_name (str): State name to search for

    Prints:
    - City names retrieved from the database, sorted by cities.id
    """
    try:
        # Connect to the MySQL server
        db = MySQLdb.connect(
            user=username,
            passwd=password,
            db=database,
            host="localhost",
            port=3306
        )

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query with user input using parameterized query
        query = """
        SELECT cities.name FROM cities
        JOIN states ON cities.state_id = states.id
        WHERE states.name = %s
        ORDER BY cities.id ASC
        """

        # Execute the query
        cursor.execute(query, (state_name,))
        rows = cursor.fetchall()

        # Print the city names separated by commas
        print(", ".join(row[0] for row in rows))

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL server: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print(
            """
            Usage: {} <mysql username> <mysql password>
            <database name> <state name>
            """.format(sys.argv[0]))
        sys.exit(1)

    # Extract command-line arguments
    username = sys.argv[1]
    password = sys.argv[2]
    database = sys.argv[3]
    state_name = sys.argv[4]

    list_cities_by_state(username, password, database, state_name)
