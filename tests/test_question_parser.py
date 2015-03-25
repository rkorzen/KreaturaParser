from unittest import TestCase
from kparser import question_parser
from elements import Question
__author__ = 'KorzeniewskiR'


class TestQuestion_parser(TestCase):
    def test_simple_single_question_parser(self):
        line = "Q S Q0 Treść"
        expected = Question("Q0")
        expected.typ = "S"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_multi_question_parser(self):
        line = "Q M Q0 Treść"
        expected = Question("Q0")
        expected.typ = "M"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_layout_question_parser(self):
        line = "Q L Q0 Treść"
        expected = Question("Q0")
        expected.typ = "L"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_question_parser(self):
        line = "Q G Q0 Treść"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_old_question_parser(self):
        line = "Q SDG Q0 Treść"
        expected = Question("Q0")
        expected.typ = "SDG"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_basket_question_parser(self):
        line = "Q B Q0 Treść"
        expected = Question("Q0")
        expected.typ = "B"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_basket_old_question_parser(self):
        line = "Q LHS Q0 Treść"
        expected = Question("Q0")
        expected.typ = "LHS"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_table_question_parser(self):
        line = "Q T Q0 Treść"
        expected = Question("Q0")
        expected.typ = "T"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_numeric_question_parser(self):
        line = "Q N Q0 Treść"
        expected = Question("Q0")
        expected.typ = "N"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_parser(self):
        line = "Q O Q0 Treść"
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_with_size_parser(self):
        line = "Q O90_4 Q0 Treść"
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)