##!/usr/bin/python3

""""importing the json"""
import json

"""
founction that writes an oject to a text file
using JSON reprsentation
"""


def save_to_json_file(my_obj, filename):
    """
    returns the JSON representation of an object
    """

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(my_obj, f)
