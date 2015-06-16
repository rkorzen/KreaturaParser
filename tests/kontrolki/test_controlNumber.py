from elements import ControlNumber
from lxml import etree
from tests.testing_tools import KreaturaTestCase

__author__ = 'KorzeniewskiR'


class TestControlNumber(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" name="Q2 | test" require="true" results="true" style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)