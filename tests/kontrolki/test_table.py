from KreaturaParser.elements import ControlTable, Row, Cell, ControlLayout
from KreaturaParser.tests.testing_tools import KreaturaTestCase
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestTable(KreaturaTestCase):

    def setUp(self):
        self.table = ControlTable('T1')

    def test_table(self):
        """<control_table id="A5_table" random="false" rotation="false" rrdest="row" style="">"""
        self.assertEqual(self.table.id, 'T1')
        self.assertEqual(self.table.random, 'false')
        self.assertEqual(self.table.rotation, 'false')
        self.assertEqual(self.table.rrdest, 'row')
        self.assertEqual(self.table.style, '')
        self.assertEqual(self.table.rows, [])
        self.assertEqual(self.table.xml, None)

    def test_add_row(self):
        row = Row()
        self.table.add_row(row)
        self.assertEqual(self.table.rows, [row])

    def test_add_row_and_there_is_no_row_instance(self):
        row = "row"
        self.assertRaises(TypeError, self.table.add_row, row)

    def test_to_xml(self):
        want = """<control_table id="T1" random='false' rotation='false' rrdest='row' style=''><row forcestable='true'
         style=''><cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default"
         style=""><content></content></control_layout></cell></row></control_table>"""

        cl = ControlLayout('Q1')
        cell = Cell()
        row = Row()

        cell.add_control(cl)
        row.add_cell(cell)

        self.table.add_row(row)
        self.table.to_xml()

        got = etree.tostring(self.table.xml)
        self.assertXmlEqual(got, want)

    def test_to_xml_no_row(self):
        want = """<control_table id="T1" random='false' rotation='false' rrdest='row' style=''><row forcestable='true'
         style=''><cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default"
         style=""><content></content></control_layout></cell></row></control_table>"""

        # cl = ControlLaout('Q1')
        # cell = Cell()
        row = Row()
        #
        # cell.add_control(cl)
        # row.add_cell(cell)

        # self.table.add_row(row)
        # self.table.to_xml()
        # self.table.to_xml()
        # got = etree.tostring(self.table.xml)
        # # self.assertXmlEqual(got, want)
        self.assertRaises(ValueError, self.table.to_xml)

    def test_to_xml_no_cell_on_row(self):
        want = """<control_table id="T1" random='false' rotation='false' rrdest='row' style=''><row forcestable='true'
         style=''><cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default"
         style=""><content></content></control_layout></cell></row></control_table>"""

        # cl = ControlLaout('Q1')
        # cell = Cell()
        row = Row()
        #
        # cell.add_control(cl)
        # row.add_cell(cell)

        self.table.add_row(row)
        # self.table.to_xml()
        # self.table.to_xml()
        # got = etree.tostring(self.table.xml)
        # # self.assertXmlEqual(got, want)
        self.assertRaises(ValueError, self.table.to_xml)
