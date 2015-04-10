from unittest import TestCase
from parsers import program_parser
__author__ = 'KorzeniewskiR'


class TestProgram_parser(TestCase):


    def test_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)


    def test_two_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nEND PROGRAM"
        #input_ = "B B0\nBEGIN PROGRAM\nA=1\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nB=2\nEND PROGRAM"

        expected = "B B0\nB B1\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)


    def test_for_loop(self):
        input_ = """B B0
BEGIN PROGRAM

for i in range(2):
    print('''P P{0}'''.format(i))

END PROGRAM"""

        expected = "B B0\nP P0\nP P1\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)
