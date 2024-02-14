#!/usr/bin/python3
"""
A module that test differents behaviors
of the Base class
"""
import unittest
import pep8
import os
from models.base import Base 
from models.rectangle import Rectangle
from models.square import Square

class TestBase(unittest.TestCase):
    """
    Test module for Base class
    """

    def test_pep8_base(self):
        """
        Test that checks PEP8
        """
        syntax = pep8.StyleGuide(quit=True)
        check = syntax.check_files(['models/base.py'])
        self.assertEqual(
            check.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_id_as_none(self):
        """No-arg constructor"""
        b1 = Base()
        self.assertEqual(b1.id, 1)
        b2 = Base()
        self.assertEqual(b2.id, 2)
        b3 = Base()
        self.assertEqual(b3.id, 3)

    def test_id_as_positive(self):
        """Constructor with positive argument"""
        b4 = Base(10)
        self.assertEqual(b4.id, 10)
        b5 = Base(99)
        self.assertEqual(b5.id, 99)

    
    def test_id_as_negative(self):
        """Constructor with negative argument"""
        b6 = Base(-10)
        self.assertEqual(b6.id, -10)
        b7 = Base(-99)
        self.assertEqual(b7.id, -99)


    def test_id_as_float(self):
        """Constructor with float argument"""
        b8 = Base(10.5)
        self.assertEqual(b8.id, 10.5)
        b9 = Base(99.5)
        self.assertEqual(b9.id, 99.5)

    def test_to_json_string(self):
        """
        Test a normal to_json_string functionality
        """
        rect_data = {'id': 31, 'x': 14, 'y': 11, 'width': 3, 'height': 3}
        json_data = Base.to_json_string([rect_data])

        self.assertTrue(isinstance(rect_data, dict))
        self.assertTrue(isinstance(json_data, str))
        self.assertCountEqual(
            json_data,
            '{["id": 31, "x": 14, "y": 11, "width": 3, "height": 3]}'
        )

    def test_wrong_to_json_string(self):
        """
        Test a wrong functionality of the
        to_json_string method
        """
        json_data = Base.to_json_string(None)
        self.assertEqual(json_data, "[]")

        warn = ("to_json_string() missing 1 required positional argument: " +
                "'list_dictionaries'")

        with self.assertRaises(TypeError) as msg:
            Base.to_json_string()

        self.assertEqual(warn, str(msg.exception))

        warn = "to_json_string() takes 1 positional argument but 2 were given"

        with self.assertRaises(TypeError) as msg:
            Base.to_json_string([{43, 87}], [{22, 17}])

        self.assertEqual(warn, str(msg.exception))

    def test_wrong_save_to_file(self):
        """
        Test the save_to_file method
        """
        with self.assertRaises(AttributeError) as msg:
            Base.save_to_file([Base(1), Base(2)])

        self.assertEqual(
             "'Base' object has no attribute 'to_dictionary'",
             str(msg.exception)
        )

    def test_load_from_file(self):
        """
        Test the load_from_file method
        """
        if os.path.exists("Base.json"):
            os.remove("Base.json")

        if os.path.exists("Rectangle.json"):
            os.remove("Rectangle.json")

        if os.path.exists("Square.json"):
            os.remove("Square.json")

        rect_output = Rectangle.load_from_file()
        self.assertEqual(rect_output, [])

        square_output = Square.load_from_file()
        self.assertEqual(square_output, [])

        warn = "load_from_file() takes 1 positional argument but 2 were given"

        with self.assertRaises(TypeError) as msg:
            Rectangle.load_from_file('Monty Python')

        self.assertEqual(warn, str(msg.exception))

    def test_create(self):
        """
        Test the create method
        """
        with self.assertRaises(TypeError) as msg:
            warn = Rectangle.create('Monty Python')

        self.assertEqual(
            "create() takes 1 positional argument but 2 were given",
            str(msg.exception)
        )

