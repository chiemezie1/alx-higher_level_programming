##!/usr/bin/python3

""""importing the json"""
import json

"""
founction that writes an oject to a text file
using JSON reprsentation
"""


def save_to_json_file(my_obj, filename):
    """write an object to a text file as Json"""
    with open(filename, mode='w') as file:
        file.write(json.dump(my_obj))
