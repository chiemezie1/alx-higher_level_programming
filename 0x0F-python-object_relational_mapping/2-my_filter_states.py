#!/usr/bin/python3
"""
A script that takes an argument and displays all values in the states
table of hbtn_0e_0_usa where name matches the argument.
"""
import MySQLdb
from sys import argv


def find_states(username, password, database, name):
    """
    A function that takes an argument and displays all values
    in the states table of hbtn_0e_0_usa where name matches
    the argument.
    """
    # Connect to the MySQL server
    db = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=username,
        passwd=password,
        db=database
    )

    # Create a cursor object
    cursor = db.cursor()

    # Execute the query
    cursor.execute(
        """
        SELECT * FROM states
        WHERE name LIKE BINARY %s
        ORDER BY id ASC
        """,
        (name,)
    )

    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

    # Close the cursor and database connection
    cursor.close()
    db.close()

if __name__ == "__main__":
    username = argv[1]
    password = argv[2]
    database = argv[3]
    name = argv[4]

    find_states(username, password, database, name)
