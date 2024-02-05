#!/usr/bin/python3

""""checks if an object is exactly an instance of

the specified class

Returns: True if the object is exactly an instance of

"""


def is_same_class(obj, a_class):
    """Checks if an object is exactly an instance of
    the specified class
    """
    return type(obj) == a_class
