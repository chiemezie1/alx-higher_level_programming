#!/usr/bin/python3
"""
 if the object is an instance of a class
 that inherited (directly or indirectly)
from the specified class

"""



def inherits_from(obj, a_class):
    """
    Check if the object is an instance of a class that inherited
    (directly or indirectly) from the specified class.

    :param obj: The object to be checked.
    :param a_class: The class to check against.
    :return: True if obj is an instance of a class
    inherited from a_class, False otherwise.
    """

    if type(obj) == a_class:
        return False
    return isinstance(obj, type) and issubclass(obj, a_class)
