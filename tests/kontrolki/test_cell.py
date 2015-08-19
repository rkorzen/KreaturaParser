from KreaturaParser.tests.test_parse import KreaturaTestCase
from KreaturaParser.elements import ControlLayout
from KreaturaParser.elements import Cell
from lxml import etree

__author__ = 'KorzeniewskiR'


class TestCell(KreaturaTestCase):
    def test_cell(self):
        cell = Cell()

        self.assertEqual(cell.colspan, '1')
        self.assertEqual(cell.forcestable, 'false')
        self.assertEqual(cell.rowspan, '1')
        self.assertEqual(cell.style, '')
        self.assertEqual(cell.xml, None)
        self.assertEqual(cell.control, None)

    def test_add_control(self):
        cell = Cell()
        cell.add_control('Kontrolka')

        self.assertEqual(cell.control, 'Kontrolka')

    def test_to_xml_without_cell(self):
        cell = Cell()
        self.assertRaises(ValueError, cell.to_xml)

    def test_to_xml(self):
        cell = Cell()
        left = ControlLayout('Q1')
        left.content = 'COS'
        cell.add_control(left)
        want = """<cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default" style=""><content>COS</content></control_layout></cell>"""
        cell.to_xml()
        got = etree.tostring(cell.xml).decode("utf-8")
        self.assertXmlEqual(got, want)

    def test_add_control_without_to_xml(self):
        cell = Cell()
        cell.add_control('Kontrolka')
        self.assertRaises(AttributeError, cell.to_xml)