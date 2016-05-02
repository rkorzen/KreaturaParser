from unittest import TestCase, main
from KreaturaParser.kparser import page_parser
from KreaturaParser.elements import Page


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

    def test_page_with_parent(self):
        line = "P P0 --parent:MAIN"
        got = page_parser(line)

        want = Page('P0')
        want.parent_id = "MAIN"

        self.assertEqual(got, want)

if __name__ == '__main__':
    main()
