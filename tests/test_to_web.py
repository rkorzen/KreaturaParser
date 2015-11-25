from unittest import main
from KreaturaParser.kparser import parse, print_tree
from KreaturaParser.elements import Block, Page, Question, Cafeteria, Survey
from lxml import etree
from KreaturaParser.tests.testing_tools import KreaturaTestCase
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

        expected = "    ' xxx\n    Q1.Ask()"

        self.assertEqual(expected, result)


    def test_postcode(self):
        text_input = """Q S Q1 COS
POST xxx
1 a
2 b"""
        survey = parse(text_input)
        survey.to_web()
        result = survey.web_out

        expected = "Q1.Ask()\n' xxx"

        self.assertEqual(expected, result)

