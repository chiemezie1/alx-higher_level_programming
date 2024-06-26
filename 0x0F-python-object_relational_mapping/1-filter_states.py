#!/usr/bin/python3
"""
Script that lists all states with a name starting with 'N'
from the database hbtn_0e_0_usa

Usage: ./1-filter_states.py <mysql username> <mysql password> <database name>
"""
import sys
import MySQLdb


def list_n_states(username, password, database):
    """
    Connects to MySQL server and retrieves all states from 'states' table
    with names starting with 'N'.

    Args:
    - username (str): MySQL username
    - password (str): MySQL password
    - database (str): Database name

    Prints:
    - State rows retrieved from the database
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
            SELECT * FROM states
            WHERE states.name
            LIKE BINARY 'N%'
            ORDER BY states.id ASC

            """
        )
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL server: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print(
            "Usage: {} <mysql username> <mysql password> <database name>"
            .format(sys.argv[0]))
        sys.exit(1)

    # Extract command-line arguments
    username = sys.argv[1]
    password = sys.argv[2]
    database = sys.argv[3]

    list_n_states(username, password, database)
