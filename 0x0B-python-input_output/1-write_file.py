#!/usr/bin/python3
"""
writes a string to a text file (UTF8)
Returns: the number of characters written

"""


def write_file(filename="", text=""):
    """
    write a string to a text file
    """
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(text)
        return len(text)
