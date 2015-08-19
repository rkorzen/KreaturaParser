from unittest import TestCase
from KreaturaParser.tools import show_attr

__author__ = 'KorzeniewskiR'


class Test(object):
    pass


class TestShowAttr(TestCase):

    def test_show_attr(self):
        ob = Test()
        ob.id = '1'
        result = show_attr(ob)
        expected = ["id = 1"]
        self.assertEqual(expected, result)

    def test_no_attr(self):
        ob = Test()
        result = show_attr(ob)
        expected = []

        self.assertEqual(expected, result)

    def test_attr_none(self):
        ob = Test()
        ob.foo = None

        result = show_attr(ob)
        expected = ['foo = None']

        self.assertEqual(expected, result)
