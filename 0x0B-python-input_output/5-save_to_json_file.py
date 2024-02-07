##!/usr/bin/python3

""""importing the json"""
import json

"""
founction that writes an oject to a text file
using JSON reprsentation 
"""


def save_to_json_file(my_obj, filename):
     """Founction that writes an oject to a text file"""
     with open(filename) as file:
        file.write(json.dump(my_obj))
