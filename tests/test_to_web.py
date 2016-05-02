from unittest import main
from kparser import parse, print_tree
from elements import Block, Page, Question, Cafeteria, Survey
from lxml import etree
from tests.testing_tools import KreaturaTestCase
# from KreaturaParser.tools import show_attr


class TestParse(KreaturaTestCase):

    # region block tests
    def test_precode(self):
        text_input = """Q S Q1 COS
PRE ' xxx
1 a
2 b"""
        survey = parse(text_input)
        survey.to_web()
        result = survey.web_out

        expected = "    ' xxx\n    Q1.Ask()\n"

        self.assertEqual(expected, result)


    def test_postcode(self):
        text_input = """Q S Q1 COS
POST ' xxx
1 a
2 b"""
        survey = parse(text_input)
        x = survey.childs[0].childs[0]
        survey.to_web()
        result = survey.web_out

        expected = "    Q1.Ask()\n    ' xxx\n"

        self.assertEqual(expected, result)


    def test_grid_by_slice(self):
        self.fail()