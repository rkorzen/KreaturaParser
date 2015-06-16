from unittest import TestCase, main
from kparser import page_parser
from elements import Page


class TestPageParser(TestCase):

    def test_page_parser(self):
        line = "P P0"
        result = page_parser(line)
        expected = Page("P0")
        self.assertEqual(result, expected)

    def test_page_parser_with_hide(self):
        line = 'P P0 --hide: $A1:97 == "1"'
        result = page_parser(line)
        expected = Page("P0")
        expected.hide = ' $A1:97 == "1"'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    main()
