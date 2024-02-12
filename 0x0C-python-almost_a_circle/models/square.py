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
        super.__init__(self, size, size, x, y, id)
    
    def __str__(self):
        """
        ...
        """
        return '[Square] ({:d}) {:d}/{:d} - {:d}'.format(
            self.id, self.x, self.y, self.width
        )
