from unittest import TestCase, main
from kparser import question_parser
from elements import Question


class TestQuestionParser(TestCase):
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
        expected.size = ['90', '4']
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_with_size_and_hide_parser(self):
        line = 'Q O90_4 Q0 Treść --hide:$A1="1"'
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        expected.size = ['90', '4']
        expected.hide = '$A1="1"'
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_rotation(self):
        line = "Q G Q0 Treść --rot"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.rotation = True
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_random(self):
        line = "Q G Q0 Treść --ran"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.random = True
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_random_and_hide(self):
        line = 'Q G Q0 Treść --ran --hide:$A1:1 == "1"'
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.random = True
        expected.hide = '$A1:1 == "1"'
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_single_with_parent(self):
        line = "Q S Q1 --p:Q0 Treść"
        expected = Question("Q1")
        expected.typ = "S"
        expected.content = "Treść"
        expected.parent_id = "Q0"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_with_deactivate(self):
        line = "Q O Q1 TRESC --dk:Nie wiem"
        expected = Question("Q1")
        expected.typ = "O"
        expected.content = "TRESC"
        expected.dontknow = "Nie wiem"
        result = question_parser(line)
        self.assertEqual(expected, result)

if __name__ == '__main__':
    main()