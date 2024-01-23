#!/usr/bin/python3
"""Square Class

This class defines a square with size validation.

"""


class Square:
    """Square Class"""

    def __init__(self, size=0):
        """Initialize a Square instance.

        Args:
            size (int): The size of the square.

        Raises:
            TypeError: If size is not an integer.
            ValueError: If size is less than 0.
        """
        if not isinstance(size, int):
            raise TypeError("size must be an integer")
        elif size < 0:
            raise ValueError("size must be >= 0")
        else:
            self.__size = size
