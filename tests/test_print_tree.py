from unittest import TestCase, main

from KreaturaParser.kparser import parse, print_tree


class TestPrintTree(TestCase):
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
        expected = '''B0
\tB1
\tB2
\t\tP1
\t\t\tQ1
\t\tB3
B4'''
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
        expected = '''B0
\tB1
\tB2
\t\tP1
\t\t\tQ1
\t\tB3
B4'''
        self.assertEqual(expected, result)


if __name__ == '__main__':
    main()
