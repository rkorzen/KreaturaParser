from unittest import TestCase
from elements import Cafeteria
from parsers import cafeteria_parser


class TestStatementParser(TestCase):

    def test_slash(self):
        line = "Nie wiem/trudno powiedzieć"
        expected = Cafeteria()
        expected.content = "Nie wiem/trudno powiedzieć"
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_backslash(self):
        line = r"Nie wiem\trudno powiedzieć"
        expected = Cafeteria()
        expected.content = r"Nie wiem\trudno powiedzieć"
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_cafeteria_with_nr(self):
        line = "1 cos"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "cos"
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_polish_signs(self):
        line = "1 coś coś"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_no_id(self):
        line = "coś coś"
        expected = Cafeteria()
        expected.content = "coś coś"
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_deacticate(self):
        line = "96.d coś coś"
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "coś coś"
        expected.deactivate = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_other(self):
        line = "96.c coś coś"
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "coś coś"
        expected.other = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_hide(self):
        line = '1 coś coś --hide: $A1:{0} == "1"'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.hide = ' $A1:{0} == "1"'
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_out(self):
        line = '1 coś coś --out'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.out = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_all_possible(self):
        line = '96.d Procter&Gamble --hide: $A1:{0} == "1" --out'
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "Procter&Gamble"
        expected.hide = ' $A1:{0} == "1"'
        expected.deactivate = True
        expected.out = True
        result = cafeteria_parser(line)
        print(result.content)
        self.assertEqual(expected, result)
