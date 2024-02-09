#!/usr/bin/python3
"""
Base class for all class
"""

from os import path
import json


class Base():
    """
    Base class for all class

    private class attribute __nb_objects
    public class attribute id

    """
    __nb_objects = 0

    def __init__(self, id=None):
        if id is not None:
            self.id = id
        else:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects
