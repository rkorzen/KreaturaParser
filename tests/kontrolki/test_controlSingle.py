from elements import ControlSingle, Cafeteria
from lxml import etree
from tests.testing_tools import KreaturaTestCase
__author__ = 'KorzeniewskiR'


class TestControlSingle(KreaturaTestCase):
    def test_to_xml(self):
        single = ControlSingle('Q1')
        caf = Cafeteria()
        caf.id = '1'
        caf.content = "A"
        single.cafeteria = [caf]

        single.name = "test"
        single.to_xml()
        got = etree.tostring(single.xml)
        want = '''<control_single id="Q1" itemlimit="0" layout="vertical" name="test" random="false" require="true" results="true" rotation="false" style=""><list_item id="1" name="" style=""><content>A</content></list_item></control_single>'''

        self.assertXmlEqual(got, want)

