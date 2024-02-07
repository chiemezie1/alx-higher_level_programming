#!/usr/bin/python3

""""importing the json"""
import json


"""
founction that returns the JSON representation
of an object
Returnss the JSON representation of an object
"""


def to_json_string(my_obj):
    """
    returns the JSON representation of an object
    """

    return json.dumps(my_obj)
