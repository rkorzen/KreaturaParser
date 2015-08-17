from unittest import TestCase

from KreaturaParser.tools import clean_labels

__author__ = 'KorzeniewskiR'


class TestClean_labels(TestCase):
    def test_clean_labels_img(self):
        in_ = '''<img src='public/koncept_1.jpg' alt="koncept_1">koncept 1<br> <span style="color:red">cos</span>'''
        want = 'koncept 1 cos'
        got = clean_labels(in_)
        self.assertEqual(got, want)