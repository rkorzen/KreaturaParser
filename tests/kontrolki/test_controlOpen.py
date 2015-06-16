from elements import ControlOpen
from lxml import etree
from tests.testing_tools import KreaturaTestCase

__author__ = 'KorzeniewskiR'


class TestControlOpen(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlOpen('Q1')
        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_open id="Q1" length="25" lines="1" mask=".*" name="Q1"
require="true" results="true" style=""><content/></control_open>'''

        self.assertXmlEqual(got, want)
