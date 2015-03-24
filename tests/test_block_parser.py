from unittest import TestCase
from kparser import block_parser
from kparser import Block
__author__ = 'KorzeniewskiR'


class TestBlock_parser(TestCase):
    def test_simple_block(self):
        line = "B B0"
        result = block_parser(line)
        expected = Block("B0")

        self.assertEqual(result, expected)


