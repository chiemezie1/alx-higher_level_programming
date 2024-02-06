#!/usr/bin/python3
"""
Public instance method: def area(self)
Rases an exception

Public instance method:
def integer_validator(self, name, value)

"""


class BaseGeometry:
    """
    Public instance method: def area(self)
    Rases an exception
    Exception: area() is not implemented

    public instance method:
    def integer_validator(self, name, value)

    if value is less or equal to 0: raise a ValueError
    if value is not an integer: raise a TypeError exception

    """

    @property
    def area(self):
        raise Exception("area() is not implemented")

    @property
    def integer_validator(self, name, value):
        if type(value) is not int:
            raise TypeError("{} must be an integer".format(name))
        if value <= 0:
            raise ValueError("{} must be greater than 0".format(name))
