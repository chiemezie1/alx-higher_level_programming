#!/usr/bin/python3
""" importing Json """
import json

"""
function that returns python object
represented as a JSON object
"""


def from_json_string(my_str):
    """
    returns the JSON representation of an object
    """
    return json.loads(my_str)
