from unittest import TestCase
from parsers import program_parser
__author__ = 'KorzeniewskiR'


class TestProgram_parser(TestCase):


    def test_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0"
        result = program_parser(input_)

        self.assertEqual(expected, result)


    def test_two_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0"
        result = program_parser(input_)

        self.assertEqual(expected, result)
