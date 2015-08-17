from unittest import TestCase, main
from KreaturaParser.elements import Cafeteria
from KreaturaParser.parsers import cafeteria_parser


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

    def test_with_screenout(self):
        line = '1 coś coś --so'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.screenout = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_with_gotonext(self):
        line = '1 coś coś --gn'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.gotonext = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_all_possible(self):
        line = '96.d Procter&Gamble --hide: $A1:{0} == "1" --so'
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "Procter&Gamble"
        expected.hide = ' $A1:{0} == "1"'
        expected.deactivate = True
        expected.screenout = True
        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_screeonout_info(self):
        line = '1 cos --so'

        expected = Cafeteria()
        expected.id = '1'
        expected.content = 'cos'
        expected.screenout = True

        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

    def test_screeonout_info_2(self):
        line = '1 a --so'

        expected = Cafeteria()
        expected.id = '1'
        expected.content = 'a'
        expected.screenout = True

        result = cafeteria_parser(line)
        self.assertEqual(expected, result)

if __name__ == '__main__':
    main()
