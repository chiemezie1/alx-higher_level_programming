#!/usr/bin/python3
""" importing Json """
import json

"""
function that creates an Object from a 'JSON file'
"""


def load_from_json_file(filename):
    """
    creates an Object from a 'JSON file'
    """
    with open(filename, encoding="utf-8") as f:
        return json.load(f)
