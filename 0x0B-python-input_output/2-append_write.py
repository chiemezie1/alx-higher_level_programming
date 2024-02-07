#!/usr/bin/python3
"""
Appends a string at the end of a text file (UTF8)
Returns the number of characters added

"""


def append_write(filename="", text=""):
    """
    Appends a string at the end of a text file (UTF8)
    Returns the number of characters added
    """

    with open(filename, 'a', encoding="utf-8") as f:
        f.write(text)
        return len(text)
