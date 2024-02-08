#!/usr/bin/python3
"""
function that prints a text with 2 new lines after
"""


def text_indentation(text):
    """
    function that prints a text with 2 new lines after
    """
    if type(text) is not str:
        raise TypeError("text must be a string")
    for i in text:
        if i in ['.', '?', ':']:
            print(i)
            print()
        else:
            print(i, end="")
