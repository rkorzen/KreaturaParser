# coding: utf-8
from unittest import TestCase
from KreaturaParser.tools import wersjonowanie_plci
__author__ = 'KorzeniewskiR'


class TestWersjonowanie_plci(TestCase):
    def test_wersjonowanie_plci(self):
        in_ = 'Pan(i) Pana(i) Panem(nią)'
        got = wersjonowanie_plci(in_)
        want = '#SEX_M# #SEX_D# #SEX_N#'
        self.assertEqual(got, want)

