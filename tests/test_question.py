from unittest import TestCase
from elements import Question
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestQuestion(TestCase):
    def test_to_xml(self):
        question = Question('Q1')
        question.to_xml()
        result = etree.tostring(question.xml, pretty_print=True)
        expected = etree.fromstring('<question id="Q1" name=""/>')
        expected = etree.tostring(expected, pretty_print=True)

        self.assertEqual(expected, result)
