from lxml import etree
from unittest import TestCase
from KreaturaParser.elements import Page


class TestPage(TestCase):

    def test_class_exist(self):
        p = Page('P1')
        self.assertIsInstance(p, Page)

    def test_class_init(self):
        p = Page('P1')
        self.assertEqual('P1', p.id)

    def test_build_xml(self):
        e_xml = etree.tostring(etree.fromstring('<page id="P1" hideBackButton="false" name=""></page>'))
        p = Page('P1')

        p.to_xml()

        xml = etree.tostring(p.xml)
        self.assertEqual(e_xml, xml)
