#!/usr/bin/python3
"""
Script to list all states from the database hbtn_0e_0_usa.

Usage: ./0-select_states.py <mysql username> <mysql password> <database name>
"""
import sys
import MySQLdb


def list_states(username, password, database):
    """
    Connects to MySQL server and retrieves all states from 'states' table.

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
        cursor.execute("SELECT * FROM states ORDER BY id ASC")
        rows = cursor.fetchall()

        # Print the rows
        for row in rows:
            print(row)

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        # Close the cursor and the connection
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

    list_states(username, password, database)
