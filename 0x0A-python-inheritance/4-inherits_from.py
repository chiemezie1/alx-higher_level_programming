#!/usr/bin/python3
"""
 if the object is an instance of a class
 that inherited (directly or indirectly)
from the specified class

"""



def inherits_from(obj, a_class):
    """
    Checks if an object is an instance of,
    or if the object is an instance of a class
    that inherited from, the specified class.

    Returns: True if the object is an instance of a
    class that inherited from the specified class;
    otherwise False.
    
    """

    if isinstance(obj, a_class) and \
       issubclass(a_class, obj.__class__) is False:
        return True

    return False