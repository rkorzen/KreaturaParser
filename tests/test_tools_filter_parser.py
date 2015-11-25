from unittest import TestCase

from KreaturaParser.tools import filter_parser

class TestFilter_parser(TestCase):
    def test_ibis_goto_next_translation_ask_if_checked(self):
        input_ = 'if($Q1:3 == "1");else;goto next;endif'
        result = filter_parser(input_)
        expected = '\n    if Q1.ContainsAny("x3") then {}.Ask()\n\n'
        self.assertEqual(expected, result)

    def test_ibis_goto_next_translation_ask_if_not_checked(self):
        """Zadaj jeśli odp nie zaznaczona"""
        input_ = 'if($Q1:3 == "1");goto next;else;endif'
        result = filter_parser(input_)
        expected = '\n    if not Q1.ContainsAny("x3") then {}.Ask()\n\n'
        self.assertEqual(expected, result)

    def test_dim_style_precode(self):
        input_ = "' if cos the cos"
        result = filter_parser(input_)
        expected = "' if cos the cos"
        self.assertEqual(expected, result)
