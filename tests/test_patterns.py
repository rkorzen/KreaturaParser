# coding: utf-8
from KreaturaParser.tests.testing_tools import KreaturaTestCase
from KreaturaParser.parsers import Patterns
import re
class TestPatterns(KreaturaTestCase):

    def test_goto_pattern(self):
        line1 = "--goto:Q1_p"
        line2 = "1 A --goto:Q1_p"
        line3 = "1 A --goto:Q1_p --hide:cos"
        line4 = "1 A--goto:Q1_p--hide:cos"
        line5 = "1 A--goto: Q1_p--hide:cos"
        pattern = Patterns.goto_pattern

        r1 = pattern.findall(line1)
        r2 = pattern.findall(line2)
        r3 = pattern.findall(line3)
        r4 = pattern.findall(line4)
        r5 = pattern.findall(line5)

        expected1 = "[('', 'Q1_p')]"
        expected2 = "[(' ', 'Q1_p')]"

        self.assertEqual(expected1, str(r1))
        self.assertEqual(expected1, str(r2))
        self.assertEqual(expected1, str(r3))
        self.assertEqual(expected1, str(r4))
        self.assertEqual(expected2, str(r5))


    def test_hide_pattern(self):
        line1 = 'A --hide:$P4B:{0} == "1"'
        line2 = 'A--hide:$P4B:{0} == "1"'
        pattern = Patterns.hide_pattern

        r1 = pattern.findall(line1)
        r2 = pattern.findall(line2)

        expected = ['$P4B:{0} == "1"']
        self.assertEqual(expected, r1)
        self.assertEqual(expected, r2)


    def test_cafeteria_patter(self):
        line1 = 'A--hide:$P4B:{0} == "1"'
        line2 = 'A --hide:$P4B:{0} == "1"'
        line3 = '1 coś coś --hide:$A1:{0} == "1"'
        pattern = Patterns.caf_pattern

        r1 = pattern.match(line1)
        r2 = pattern.match(line2)
        r3 = pattern.match(line3)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)

