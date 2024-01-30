#!/usr/bin/python3
"""Defines a Rectangle class"""


class Rectangle:
    """Represent a rectangle

      __init__ Instantiation with optional width and height

    @width: width of the rectangle
    property width getter and setter
    Rasie: an exception if width is not an integer or not a positive integer


    @height: height of the rectangle
    property height getter and setter
    Raise: an exception if height is not an integer or not a positive integer

    """

    def __init__(self, width=0, height=0):
        """Instantiation with optional width and height
        Args:
            width: width of the rectangle
            height: height of the rectangle
        """
        self.width = width
        self.height = height

    @property
    def width(self):
        """width getter"""
        return self.__width

    @width.setter
    def width(self, value):
        """width setter"""
        if not isinstance(value, int):
            raise TypeError("width must be an integer")
        if value < 0:
            raise ValueError("width must be >= 0")
        self.__width = value

    @property
    def height(self):
        """height getter"""
        return self.__height

    @height.setter
    def height(self, value):
        """height setter"""
        if not isinstance(value, int):
            raise TypeError("height must be an integer")
        if value < 0:
            raise ValueError("height must be >= 0")
        self.__height = value
