#!/usr/bin/python3
def add_integer(a, b=98):
    """A function that adds 2 integers
    
    Return: The addition of a and b
    Raises: TypeError if a or b is not an integer
    
    """
    if not isinstance(a, (int, float)):
        raise TypeError("a must be an integer")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be an integer")
    return int(a) + int(b)
