from unittest import TestCase
from KreaturaParser.elements import Cafeteria, make_caf_to_dim

__author__ = 'KorzeniewskiR'



class TestMake_caf_to_dim(TestCase):

    def setUp(self):
        self.lista = []
        caf1, caf2 = Cafeteria(), Cafeteria()
        caf1.id = '1'
        caf2.id = '2'
        caf1.content = 'A'
        caf2.content = 'B'

        self.lista.append(caf1)
        self.lista.append(caf2)


    def test_make_caf_to_dim(self):
        got = make_caf_to_dim(self.lista)
        want = '''x1 "A",\nx2 "B"\n'''
        self.assertEqual(got, want)

