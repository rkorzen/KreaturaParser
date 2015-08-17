# from unittest import TestCase
from KreaturaParser.tests.testing_tools import KreaturaTestCase
from KreaturaParser.elements import Block
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestBlock(KreaturaTestCase):

    def test_class_exist(self):
        b = Block('B1')
        self.assertIsInstance(b, Block)

    def test_class_init(self):
        b = Block('B1')
        self.assertEqual('B1', b.id)

    def test_build_xml(self):
        e_xml = etree.tostring(etree.fromstring('<block id="B1" name="" quoted="false" random="false" rotation="false">'
                                                '<block id="B2" name="" quoted="false" random="false" rotation="false">'
                                                '</block></block>'))
        b1 = Block('B1')
        b2 = Block('B2')
        b1.childs.append(b2)
        b1.to_xml()

        xml = etree.tostring(b1.xml)
        self.assertEqual(e_xml, xml)

    def test_quoted(self):
        b = Block('B1')
        b.quoted = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="true" random="false" rotation="false"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)

    def test_random(self):
        b = Block('B1')
        b.random = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="false" random="true" rotation="false"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)

    def test_rotation(self):
        b = Block('B1')
        b.rotation = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="false" random="false" rotation="true"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)
