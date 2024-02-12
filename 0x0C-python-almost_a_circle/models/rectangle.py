#!/usr/bin/python3
"""
class Rectangle that inherits from Base
"""

#from models.base import Base
from base import Base


class Rectangle(Base):
    def __init__(self, width, height, x=0, y=0, id=None):
        self.check_integers_value(width, "width")
        self.check_integers_value(height, "height")
        self.check_integers_value(x, "x")
        self.check_integers_value(y, "y")

        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y

        super().__init__(id)

    @property
    def width(self):
        """
        width getter
        """
        return self.__width

    @width.setter
    def width(self, value):
        """
        width setter
        """
        self.check_integers_value(value, "width")
        self.__width = value

    @property
    def height(self):
        """
        height getter
        """
        return self.__height

    @height.setter
    def height(self, value):
        """
        height setter
        """
        self.check_integers_value(value, "height")
        self.__height = value

    @property
    def x(self):
        """
        x getter
        """
        return self.__x

    @x.setter
    def x(self, value):
        """
        x setter
        """
        self.check_integers_value(value, "x")
        self.__x = value

    @property
    def y(self):
        """
        y getter
        """
        return self.__y

    @y.setter
    def y(self, value):
        """
        y setter
        """
        self.check_integers_value(value, "y")
        self.__y = value

    def check_integers_value(self, value, param):
        """
        check if value is an integer and > 0
        """
        if type(value) is not int:
            raise TypeError(f"{param} must be an integer")

        if value <= 0 and param in ('width', 'height'):
            raise ValueError(f"{param} must be > 0")

        if value < 0 and param in ('x', 'y'):
            raise ValueError(f"{param} must be >= 0")
    
    @property
    def area(self):
        """
        returns the area value of the Rectangle instance
        """
        return self.__height * self.__width

    @property
    def display(self):
        """
        prints in stdout the Rectangle instance with the character #
        """
        if self.__y > 0:
            print("\n" * self.__y, end="")
        for _ in range(self.__height):
            if self.__x > 0:
                print(" " * self.__x, end="")
            print("#" * self.__width)
       
    def __str__(self):
        """
        overriding the __str__ method
        returns [Rectangle] (<id>) <x>/<y> - <width>/<height>
        """

        id = self.id
        x = self.__x
        y = self.__y
        width = self.__width
        height = self.__height

        return  "[Rectangle] ({:d}) {:d}/{:d} - {:d}/{:D}".format(id, x, y, width, height)
    
    @property
    def update(self, *args):
        """
        update the rectangle class, assigns an argument to each attribute
        """
        self.id = args[0]
        self.__width = args[1]
        self.__height = args[2]
        self.__x = args[3]
        self.__y = args[4]


