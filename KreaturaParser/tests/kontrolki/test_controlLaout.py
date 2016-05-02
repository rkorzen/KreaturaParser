from KreaturaParser.elements import ControlLayout
from lxml import etree
from KreaturaParser.tools import KreaturaTestCase


class TestControlLaout(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlLayout('Q1')
        c.to_xml()
        result = etree.tostring(c.xml, pretty_print=True)

        expected = etree.fromstring('<control_layout id="Q1" layout="default" style=""><content/></control_layout>')
        expected = etree.tostring(expected, pretty_print=True)

        self.assertXmlEqual(expected, result)

    def test_content_in_kwargs(self):
        c = ControlLayout('Q1', **{'content': 'COS'})
        c.to_xml()
        want = '<control_layout id="Q1" layout="default" style=""><content>COS</content></control_layout>'
        got = etree.tostring(c.xml)

        self.assertXmlEqual(got, want)
