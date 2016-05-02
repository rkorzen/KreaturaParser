from unittest import TestCase
from KreaturaParser.tools import build_precode
from lxml import etree


class TestBuildPrecode(TestCase):

    def test_simple_precode(self):
        input_ = '$A1 = "10"'
        result = build_precode(input_, 'precode')
        result = etree.tostring(result)

        expected = etree.Element('precode')
        expected.text = etree.CDATA('$A1 = "10"')
        expected = etree.tostring(expected)

        self.assertEqual(expected, result)

    def test_value_error(self):
        input_ = 'if (cos);endif'
        self.assertRaises(ValueError, build_precode, input_, 'precode')

    def test_build_precode_not_ibis(self):
        input_ = "if cos then Q1.Ask()"
        result = build_precode(input_, 'precode', "dim")
        self.assertEquals(input_, result)


    def test_build_precode_not_ibis_many_lines(self):
        input_ = 'dim x;x="";if cos then x="a"'
        result = build_precode(input_, 'precode', "dim")

        expected  = '''dim x
x=""
if cos then x="a"'''
        self.assertEquals(expected, result)