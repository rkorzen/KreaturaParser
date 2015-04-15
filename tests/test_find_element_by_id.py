from unittest import TestCase
from tools import find_by_id
from kparser import parse
from elements import Question
__author__ = 'KorzeniewskiR'


class TestFindById(TestCase):
    def test_find_by_id(self):
        input_ = """B B0
B B2
P P2

P P1
Q S Q1 A

"""

        survey = parse(input_)

        qr = find_by_id(survey, 'Q1')

        qe = Question('Q1')
        qe.typ = 'S'
        qe.content = 'A'

        self.assertEqual(qe, qr)