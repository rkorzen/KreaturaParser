from unittest import TestCase
from kparser import page_parser, Page
__author__ = 'rkorzen'


class TestPage_parser(TestCase):
    def test_page_parser(self):
        line = "P P0"
        result = page_parser(line)
        expected = Page("P0")

        self.assertEqual(result, expected)