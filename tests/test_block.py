from unittest import TestCase
from elements import Block
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestBlock(TestCase):

    def test_class_exist(self):
        b = Block('B1')
        self.assertIsInstance(b, Block)

    def test_class_init(self):
        b = Block('B1')
        self.assertEqual('B1', b.id)

    def test_build_xml(self):
        e_xml = etree.tostring(etree.fromstring('<block id="B1" name="" quoted="false" random="false" rotation="false"><block id="B2" name="" quoted="false" random="false" rotation="false"></block></block>'))
        b1 = Block('B1')
        b2 = Block('B2')
        b1.childs.append(b2)
        b1.to_xml()

        xml = etree.tostring(b1.xml)
        self.assertEqual(e_xml, xml)

