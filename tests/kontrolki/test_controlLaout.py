
from elements import ControlLaout
from lxml import etree
from tests.testing_tools import KreaturaTestCase
__author__ = 'KorzeniewskiR'


class TestControlLaout(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlLaout('Q1')
        c.to_xml()
        result = etree.tostring(c.xml, pretty_print=True)

        expected = etree.fromstring('<control_layout id="Q1" layout="default" style=""><content/></control_layout>')
        expected = etree.tostring(expected, pretty_print=True)

        self.assertXmlEqual(expected, result)
