from elements import ControlNumber
from lxml import etree
from tests.testing_tools import KreaturaTestCase


__author__ = 'KorzeniewskiR'


class TestControlNumber(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_max(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.max = "1"
        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" max="1" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_min(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.min = "1"

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" min="1" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_maxsize(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.maxsize = "2"

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" maxsize="2" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)
