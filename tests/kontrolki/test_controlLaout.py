from unittest import TestCase
from elements import ControlLaout
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestControlLaout(TestCase):
    def test_to_xml(self):
        c = ControlLaout('Q1')
        c.to_xml()
        result = etree.tostring(c.xml, pretty_print=True)
        expected = etree.fromstring('<control_layout id="Q1" layout="default" style=""><content/></control_layout>')
        expected = etree.tostring(expected, pretty_print=True)
        self.assertEqual(expected, result)