from lxml import etree

from elements import ControlSingle, Cafeteria
from KreaturaParser.tests import KreaturaTestCase

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
        want = '''<control_single id="Q1" itemlimit="0" layout="vertical" name="test" random="false" require="true"
        results="true" rotation="false" style=""><list_item id="1" name="" style=""><content>A</content></list_item>
        </control_single>'''

        self.assertXmlEqual(got, want)

    def test_wartosci_nadpisane(self):
        single = ControlSingle('Q1', **{"random": 'true'})
        single.name = 'Q1 COS'

        caf = Cafeteria()
        caf.id = "1"
        caf.content = "a"

        single.cafeteria = [caf]

        single.to_xml()
        want = '<control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 COS" random="true" ' \
               'require="true" results="true" rotation="false"><list_item id="1" name="" style="">' \
               '<content>a</content></list_item></control_single>'
        got = etree.tostring(single.xml)

        self.assertXmlEqual(got, want)

    def test_no_cafeteria(self):
        single = ControlSingle('Q1', **{"random": 'true'})
        single.name = 'Q1 COS'
        self.assertRaises(ValueError, single.to_xml)
