from unittest import TestCase
from kparser import parse, print_tree


class TestPrint_tree(TestCase):
    def test_print_tree(self):
        input_ = """B B0
B B1 B0
B B2 B0
P P1
Q S Q1 cos
B B3 B2
B B4"""

        survey = parse(input_)
        result = print_tree(survey)
        expected = '''B0\n\tB1\n\tB2\n\t\tB3\n\tP1\n\t\tQ1\nB4'''
        self.assertEqual(expected, result)

    def test_print_tree_2(self):
        input_ = """B B0

B B1 B0

B B2 B0

P P1

Q S Q1 cos

B B3 B2

B B4"""

        survey = parse(input_)
        result = print_tree(survey)
        expected = '''B0\n\tB1\n\tB2\n\t\tB3\n\tP1\n\t\tQ1\nB4'''
        self.assertEqual(expected, result)