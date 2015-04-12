from unittest import TestCase
from parsers import program_parser


class TestProgramParser(TestCase):

    def test_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_two_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0\n\nB B1\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_two_not_empty_container_without_print(self):
        input_ = "B B0\nBEGIN PROGRAM\nA=1\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nB=2\nEND PROGRAM"

        expected = """B B0

B B1
"""
        result = program_parser(input_)

        self.assertEqual(expected, result)



    def test_for_loop(self):
        input_ = """B B0
BEGIN PROGRAM
def func():
    out = ""
    for i in range(2):
        out += '''P P{0}
'''.format(i)
    return out
xxx = func()
END PROGRAM"""

        expected = """B B0
P P0
P P1
"""
        result = program_parser(input_)

        self.assertEqual(expected, result)


    def test_loop_over_list(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    list = '''Ania
Hania
Lena'''.splitlines()

    out = ""
    for count, person in enumerate(list):
        out += r'''
Q O Q1_{0} Co myślisz o osobie o imieniu {1}
'''.format(count+1, person)
    return out

xxx = func()
END PROGRAM
"""
        result = program_parser(input_)
        expected = """B B0

Q O Q1_1 Co myślisz o osobie o imieniu Ania

Q O Q1_2 Co myślisz o osobie o imieniu Hania

Q O Q1_3 Co myślisz o osobie o imieniu Lena

"""

        self.assertEqual(expected, result)