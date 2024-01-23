#!/usr/bin/python3
"""Square Class

This class defines a square

"""


class square:
    """ __init__ method

    args:
        size (int): size of the square

    """

    def __init__(self, size):
        if type(size) is not int:
            raise TypeError("size must be an integer")
        if size < 0:
            raise ValueError("size must be >= 0")
        self.__size = size
