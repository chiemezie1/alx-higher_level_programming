#!/usr/bin/python3
"""
function that inserts a line of text to a file
After each line containing a specific string
"""


def append_after(filename="", search_string="", new_string=""):
    """
function that inserts a line of text to a file
After each line containing a specific string
"""

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if search_string in line:
                f.write(line + new_string)
            else:
                f.write(line)
