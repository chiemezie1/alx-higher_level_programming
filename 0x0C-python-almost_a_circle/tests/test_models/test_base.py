#!/usr/bin/python3
"""
A module that test differents behaviors
of the Base class
"""
import unittest
import pep8
import os
from models.base import Base 
# from models.rectangle import Rectangle
# from models.square import Square

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


