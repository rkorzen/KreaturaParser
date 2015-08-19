from KreaturaParser.tests.testing_tools import KreaturaTestCase
from KreaturaParser.elements import Row
from KreaturaParser.elements import Cell
from KreaturaParser.elements import ControlLayout
from lxml import etree

class TestRow(KreaturaTestCase):
    def setUp(self):
        self.row = Row()

    def test_row(self):
        self.assertEqual(self.row.cells, [])
        self.assertEqual(self.row.forcestable, 'true')
        self.assertEqual(self.row.style, '')
        self.assertEqual(self.row.xml, None)

    def test_add_cell_error(self):
        self.assertRaises(TypeError, self.row.add_cell, 'cos')

    def test_add_cell(self):
        cell = Cell()
        self.row.add_cell(cell)

        self.assertEqual(self.row.cells, [cell])

    def test_to_xml(self):
        cell = Cell()
        cl = ControlLayout('Q1')
        cell.add_control(cl)

        self.row.add_cell(cell)
        self.row.to_xml()

        want = """<row forcestable='true' style=''><cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default" style=""><content></content></control_layout></cell></row>"""
        got = etree.tostring(self.row.xml)

        self.assertXmlEqual(got, want)