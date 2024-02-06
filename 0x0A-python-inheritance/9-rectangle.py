#!/usr/bin/python3
"""
A class Rectangle that inherits from BaseGeometry
"""


BaseGeometry = __import__('7-base_geometry').BaseGeometry


class Rectangle(BaseGeometry):
    """
    Defines a rectangle
    properties:
        width
        height
        area
        __str__
    """

    def __init__(self, width, height):
        """
        Initializes a rectangle
        """
        self.integer_validator("width", width)
        self.integer_validator("height", height)
        self.__width = width
        self.__height = height

    @property
    def area(self):
        return self.__width * self.__height

    @property
    def __str__(self):
        return "[Rectangle] {}/{}".format(self.__width, self.__height)
