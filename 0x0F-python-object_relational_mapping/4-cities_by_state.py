#!/usr/bin/python3
"""
Script that lists all cities from the database hbtn_0e_4_usa

Usage: ./4-cities_by_state.py
    <mysql username> <mysql password> <database name>
"""
import sys
import MySQLdb


def list_cities(username, password, database):
    """
    Connects to MySQL server and retrieves all cities from 'cities' table

    Args:
    - username (str): MySQL username
    - password (str): MySQL password
    - database (str): Database name

    Prints:
    - City rows retrieved from the database
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

        # Execute the query
        cursor.execute(
            """
            SELECT cities.id, cities.name, states.name
            FROM cities
            INNER JOIN states
            ON cities.state_id = states.id
            ORDER BY cities.id ASC
            """
        )

        # Print the rows
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL server: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    database = sys.argv[3]
    list_cities(username, password, database)
