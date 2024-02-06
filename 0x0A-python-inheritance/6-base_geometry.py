#!/usr/bin/python3
"""
Public instance method: def area(self)
Rases an exception

"""


class BaseGeometry:
    """
    Rases an exception
    Exception: area() is not implemented
    """

    @property
    def area(self):
        raise Exception("area() is not implemented")
