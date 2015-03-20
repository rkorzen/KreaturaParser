from unittest import TestCase
from kparser import recognize
__author__ = 'KorzeniewskiR'


class TestBlockRecognize(TestCase):

    def test_simple_block(self):
        line = "B B0"
        result = recognize(line)
        self.assertEqual("BLOCK", result)

    def test_block_with_parrent(self):
        line = "B B0 B1"
        result = recognize(line)
        self.assertEqual("BLOCK", result)

    def test_block_with_randomize(self):
        line = "B B0 --ran"
        result = recognize(line)
        self.assertEqual("BLOCK", result)

    def test_block_with_rotation(self):
        line = "B B0 --rot"
        result = recognize(line)
        self.assertEqual("BLOCK", result)

    def test_block_with_hide(self):
        line = 'B B0 --hide: $A0:{0} == "1"'
        result = recognize(line)
        self.assertEqual("BLOCK", result)

    def test_block_all_possible(self):
        line = 'B B0 B1 --rot --hide: $A0:{0} == "1"'
        result = recognize(line)
        self.assertEqual("BLOCK", result)


    def test_block_error(self):
        line = 'B B0 B1 -rot'
        result = recognize(line)
        self.assertEqual(None, result)

    def test_ran_rot_error(self):
        line = 'B B0 B1 --rot --ran'
        result = recognize(line)
        self.assertEqual(None, result)


class TestPageRecognize(TestCase):


    def test_simple_page(self):
        line = "P P0"
        result = recognize(line)
        self.assertEqual("PAGE", result)

    def test_page_with_hide(self):
        line = 'P P0 --hide:$A1:{0} == "1"'
        result = recognize(line)
        self.assertEqual("PAGE", result)

    def test_page_with_rot(self):
        """Może z czasem ta rotacja bedzie potrzebna"""
        line = 'P P0 --rot --hide:$A1:{0} == "1"'
        result = recognize(line)
        self.assertEqual(None, result)


class TestSwitchRecognize(TestCase):
    def test_switch(self):
        line = "_"
        self.assertEqual("SWITCH", recognize(line))

    def test_switch_with_spaces(self):
        line = "_  "
        self.assertEqual("SWITCH", recognize(line))


    def test_switch_double__(self):
        line = "__  "
        self.assertEqual(None, recognize(line))


class TestQuestionRecoginize(TestCase):

    def test_simple_single(self):
        line = "Q S Q1 Treść"
        self.assertEqual("QUESTION", recognize(line))