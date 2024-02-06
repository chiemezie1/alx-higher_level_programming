#!/usr/bin/python3
"""
A class Square that defines a square
"""


Rectangle = __import__('9-rectangle').Rectangle


class Square(Rectangle):
    """
    Defines a square
    """

    def __init__(self, size):
        """
        Initializes a square
        """
        self.integer_validator("size", size)
        super().__init__(size, size)
        self.__size = size
