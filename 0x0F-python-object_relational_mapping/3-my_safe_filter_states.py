#!/usr/bin/python3
"""
Script that takes in an argument and displays all values in the states table
of hbtn_0e_0_usa where name matches the argument.

Usage: ./2-my_filter_states.py <mysql username> <mysql password> <database name> <state name>
"""
import sys
import MySQLdb


def filter_states(username, password, database, state_name):
    """
    Connects to MySQL server and retrieves all states from 'states' table
    where name matches the argument.

    Args:
    - username (str): MySQL username
    - password (str): MySQL password
    - database (str): Database name
    - state_name (str): State name to search for

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

        # Execute the query with parameterized input
        query = """
        SELECT * FROM states
        WHERE states.name LIKE BINARY %s
        ORDER BY states.id ASC
        """

        # Execute the query
        cursor.execute(query, (state_name,))
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
    if len(sys.argv) != 5:
        print("Usage: {} <mysql username> <mysql password> <database name> <state name>".format(sys.argv[0]))
        sys.exit(1)

    # Extract command-line arguments
    username = sys.argv[1]
    password = sys.argv[2]
    database = sys.argv[3]
    state_name = sys.argv[4]

    filter_states(username, password, database, state_name)
