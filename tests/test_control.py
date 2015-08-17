from unittest import TestCase

from KreaturaParser.elements import Control

__author__ = 'rkorzen'


class TestControl(TestCase):

    def test_control(self):
        c = Control('id')
        self.assertIsInstance(c, Control)
        self.assertEqual(c.id, 'id')
