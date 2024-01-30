#!/usr/bin/python3
"""LockedClass module""" 


class LockedClass():
    """prevents the user from dynamically creating new instance attributes, 
    
    Except if the new instance attribute is called first_name.
    
    """


    __slots__ = ["first_name"]
