# coding: utf-8
from KreaturaParser.tools import KreaturaTestCase
from KreaturaParser.parsers import Patterns
# import re


class TestPatterns(KreaturaTestCase):

    def test_goto_pattern(self):
        line1 = "--goto:Q1_p"
        line2 = "1 A --goto:Q1_p"
        line3 = "1 A --goto:Q1_p --hide:cos"
        line4 = "1 A--goto:Q1_p--hide:cos"
        line5 = "1 A--goto: Q1_p--hide:cos"
        pattern = Patterns.goto_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1) and self.assertEqual(r1.group(0), "Q1_p")
        self.assertIsNotNone(r2) and self.assertEqual(r2.group(0), "Q1_p")
        self.assertIsNotNone(r3) and self.assertEqual(r3.group(0), "Q1_p")
        self.assertIsNotNone(r4) and self.assertEqual(r4.group(0), "Q1_p")
        self.assertIsNotNone(r5) and self.assertEqual(r5.group(0), "Q1_p")


    def test_hide_pattern(self):
        line1 = 'A --hide: $P4B:{0} == "1"'
        line2 = 'A--hide:$P4B:{0} == "1"'
        pattern = Patterns.hide_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)

        expected = '$P4B:{0} == "1"'

        self.assertEqual(expected, r1.group(1))
        self.assertEqual(expected, r2.group(1))

    def test_cafeteria_pattern(self):
        line1 = 'A--hide:$P4B:{0} == "1"'
        line2 = 'A --hide:$P4B:{0} == "1"'
        line3 = '1 coś coś --hide:$A1:{0} == "1"'
        line4 = '-1 coś'
        line5 = 'A --hide:$P4B:{0} == "1" --so'
        pattern = Patterns.caf_pattern

        r1 = pattern.match(line1)
        r2 = pattern.match(line2)
        r3 = pattern.match(line3)
        r4 = pattern.match(line4)
        r5 = pattern.match(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNotNone(r4)
        self.assertIsNotNone(r5)


    def test_screenout_pattern(self):
        line1 = "cos--so"
        line2 = "cos --so"
        line3 = "cos\t --so"
        line4 = "cos - -so"
        line5 = "cos -so"
        pattern = Patterns.screen_out_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNone(r4)
        self.assertIsNone(r5)


    def test_goto_next_pattern(self):
        line1 = "cos--gn"
        line2 = "cos --gn"
        line3 = "cos\t --gn"
        line4 = "cos - -gn"
        line5 = "cos -gn"
        pattern = Patterns.goto_next_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNone(r4)
        self.assertIsNone(r5)
