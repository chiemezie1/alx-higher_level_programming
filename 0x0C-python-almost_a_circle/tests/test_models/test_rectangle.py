#!/usr/bin/python3
"""
Test module for Rectangle
"""
import unittest
import pep8
from models.base import Base
from models.rectangle import Rectangle


class TestRectangle(unittest.TestCase):
    """
    Test module for Rectangle
    """

    def test_pep8_base(self):
        """
        Test that checks PEP8
        """
        syntax = pep8.StyleGuide(quit=True)
        check = syntax.check_files(['models/rectangle.py'])
        self.assertEqual(
            check.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_rectangle_for_base(self):
        """
        Test that checks if Rectangle inherits from Base
        """
        self.assertTrue(issubclass(Rectangle, Base))
        rect = Rectangle(1, 2)
        self.assertIsInstance(rect, Base)
        rect = Rectangle(1, 2, 3, 4, 5)
        self.assertIsInstance(rect, Base)

    def test_rectangle_for_parameters(self):
        """
        Test that checks if Rectangle has the correct parameters
        """
        rect = Rectangle(1, 2)
        rect1 = Rectangle(2, 3, 4, 5, 3)

        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 2)
        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 0)
        self.assertEqual(rect.id, 2)

        self.assertEqual(rect1.width, 2)
        self.assertEqual(rect1.height, 3)
        self.assertEqual(rect1.x, 4)
        self.assertEqual(rect1.y, 5)
        self.assertEqual(rect1.id, 3)

    def test_Rectangle_for_negative(self):
        """
        Test that checks exception for negative or zero parameters
        """
        with self.assertRaises(ValueError):
            Rectangle(-1, 2)

        with self.assertRaises(ValueError):
            Rectangle(1, 0)

    def test_Rectangle_for_string(self):
        """
        Test that checks exception for string parameters
        """
        with self.assertRaises(TypeError):
            Rectangle()

        with self.assertRaises(TypeError):
            Rectangle(1, "2")

        with self.assertRaises(TypeError):
            Rectangle(1, 2, 3, "4")

    def test_Rectangle_for_float(self):
        """
        Test that checks exception for float parameters
        """
        with self.assertRaises(TypeError):
            Rectangle(1, 5.6, 4, 7)

        with self.assertRaises(TypeError):
            Rectangle(10.3, 2)

    def test_Rectangle_for_boolen(self):
        """
        Test that checks exception for boolean parameters
        """
        with self.assertRaises(TypeError):
            Rectangle(1, 2, 3, True)

        with self.assertRaises(TypeError):
            Rectangle(False, 2)

    def test_Rectangle_for_list_tuple(self):
        """
        Test that checks exception for list parameters
        """
        with self.assertRaises(TypeError):
            Rectangle([1, 2], 2)

        with self.assertRaises(TypeError):
            Rectangle(1, (2, 3))
