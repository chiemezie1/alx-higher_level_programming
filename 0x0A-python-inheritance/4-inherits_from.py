#!/usr/bin/python3
"""
 if the object is an instance of a class
 that inherited (directly or indirectly)
from the specified class

"""



def inherits_from(obj, a_class):
    """
    Checks if an object is an instance of, or if the object is an instance of a class
    that inherited from, the specified class.

    Returns: True if the object is an instance of a class that inherited from the specified class; otherwise False.
    """
    if type(obj) is a_class:
        return False
    return issubclass(type(obj), a_class)
