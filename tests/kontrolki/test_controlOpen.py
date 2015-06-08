from unittest import TestCase
from elements import ControlOpen
from lxml import etree

__author__ = 'KorzeniewskiR'


class TestControlOpen(TestCase):
    def test_to_xml(self):
        c = ControlOpen('Q1')
        c.to_xml()
        result = str(etree.tostring(c.xml, pretty_print=True))
        expected = etree.fromstring('''<control_open id="Q1" length="25" lines="1" mask=".*" name="Q1"
require="true" results="true" style="">
<content/>
</control_open>''')
        expected = str(etree.tostring(expected, pretty_print=True))
        self.assertEqual(expected, result)