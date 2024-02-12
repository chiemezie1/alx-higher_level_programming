#!/usr/bin/python3
"""
class square that inherits from Base
"""

from models.rectangle import Rectangle

class Square(Rectangle):
    """
    class square that inherits from Base
    """
    def __init__(self, size, x=0, y=0, id=None):
        
        """
        initiating the attribute of the square from rectangle
        """
        super.__init__(size, size, x, y, id)
    
    def __str__(self):
        """
        Overloading __str__ method should return 
        """

        return '[Square] ({:d}) {:d}/{:d} - {:d}'.format(
            self.id, self.x, self.y, self.width
        )
    
    @property
    def size(self):
        """
        A public getter method 
        """
        return self.__width
    @size.setter
    def size(self, value):
        """
        A public getter method 
        """

        self.__width = value
        self.__height = value



    

    