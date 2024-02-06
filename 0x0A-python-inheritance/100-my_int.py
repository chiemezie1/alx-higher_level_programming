#!/usr/bin/python3
"""
A class MyInt that inherits from int
"""


class MyInt(int):
    """Invert the == opeartor
    """

    def __eq__(self, value):
        """Invert the == opeartor
        """
        return self.real != value

    def __ne__(self, value):
        """Invert the != opeartor
        """
        return self.real == value
