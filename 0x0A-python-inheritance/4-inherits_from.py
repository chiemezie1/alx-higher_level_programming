#!/usr/bin/python3
"""
 if the object is an instance of a class
 that inherited (directly or indirectly)
from the specified class

"""



def inherits_from(obj, a_class):
    """
    Checks if an object is an instance of a class that inherited
    (directly or indirectly) from the specified class.

    :param obj: The object to be checked.
    :param a_class: The class to check against.
    :return: True if obj is an instance of a class inherited from a_class, False otherwise.
    """
    # Check if obj is an instance of a_class or its subclass
    if isinstance(obj, a_class):
        return True

    # Check if obj's class is a subclass of a_class (directly or indirectly)
    obj_class = type(obj)
    while obj_class is not object:
        if obj_class == a_class:
            return True
        obj_class = obj_class.__base__

    return False
