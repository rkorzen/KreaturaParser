from unittest import TestCase, main
from parsers import block_parser
from elements import Block


class TestBlockParser(TestCase):
    def test_simple_block(self):
        line = "B B0"
        result = block_parser(line)
        expected = Block("B0")

        self.assertEqual(result, expected)

    def test_block_with_parent(self):
        line = "B B0 B1"
        result = block_parser(line)
        expected = Block("B0")
        expected.parent_id = "B1"
        self.assertEqual(result, expected)

    def test_block_with_hide(self):
        line = 'B B0 --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        self.assertEqual(result, expected)

    def test_block_with_rot_parent_and_hide(self):
        line = 'B B0 B1 --rot --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        expected.rotation = True
        expected.parent_id = "B1"
        self.assertEqual(result, expected)

    def test_block_with_ran_parent_and_hide(self):
        line = 'B B0 B1 --ran --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        expected.random = True
        expected.parent_id = "B1"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    main()
