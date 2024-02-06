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
        """
        Checks a integer value

        Args:
            name (str): The name of the value.
            value (int): The value.

        Raises:
            TypeError: If `value` isn't a integer.
            ValueError: If `value` is less than or equal to zero.
        """

        if type(value) is not int:
            raise TypeError(name + ' must be an integer')

        if value <= 0:
            raise ValueError(name + ' must be greater than 0')
    