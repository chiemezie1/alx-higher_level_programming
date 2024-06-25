#!/usr/bin/python3
import sys
import MySQLdb


def list_states(username, password, database):
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

    # Close the cursor and the connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    # Get the command-line arguments
    if len(sys.argv) != 4:
        print(
            "Usage: {} <mysql username> <mysql password> <database name>"
            .format(sys.argv[0]))
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    database = sys.argv[3]

    # List the states
    list_states(username, password, database)
