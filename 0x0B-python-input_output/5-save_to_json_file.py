#!/usr/bin/python3
""" importing Json """
import json

"""
founction that writes an oject to a text file
using JSON reprsentation
"""


def save_to_json_file(my_obj, filename):
    """
    Writes an object to a text file using a JSON representation.

    :param my_obj: The object to be serialized and saved.
    :param filename: The name of the file to save the JSON representation.
    """
    with open(filename, 'w') as file:
        json.dump(my_obj, file)
