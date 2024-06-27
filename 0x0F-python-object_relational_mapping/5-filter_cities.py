#!/usr/bin/python3
"""
Script script that takes in the name of a state as an argument
    and lists all cities of that state, using database hbtn_0e_4_usa

"""
import MySQLdb
from sys import argv


def filter_cities(username, password, database, state_name):
    """
    Filter cities by state name
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
            SELECT cities.name
            FROM cities
            INNER JOIN states
            ON cities.state_id = states.id
            WHERE states.name = %s
            """,
            (state_name,)
        )

        # Print the rows
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL server: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    username = argv[1]
    password = argv[2]
    database = argv[3]
    state_name = argv[4]

    filter_cities(username, password, database, state_name)
