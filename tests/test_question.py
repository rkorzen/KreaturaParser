from tests.testing_tools import KreaturaTestCase
from elements import Question
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestQuestion(KreaturaTestCase):
    def test_to_xml(self):
        question = Question('Q1')
        question.content = ""
        question.to_xml()

        result = etree.tostring(question.xml, pretty_print=True)
        expected = """  <question id="Q1" name="">
    <control_layout id="Q1.labelka" layout="default" style="">
      <content></content>
    </control_layout>
  </question>"""
        # expected = etree.tostring(expected, pretty_print=True)

        self.assertXmlEqual(result, expected)
