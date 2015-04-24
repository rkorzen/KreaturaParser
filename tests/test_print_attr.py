from unittest import TestCase, main
from tools import show_attr
__author__ = 'KorzeniewskiR'

class SomeObject():
    def __init__(self):
        self.x = 'x'
        self.y = 'y'


class TestPrint_attr(TestCase):
    def test_print_attr(self):
        element = SomeObject()
        result = show_attr(element)
        expected = sorted('x = x\ny = y'.splitlines())

        self.assertEqual(expected, result)


    def test_block(self):
        from kparser import parse
        input_ = 'B B0'
        survey = parse(input_)
        b = survey.childs[0]
        result = show_attr(b)
        expected = sorted('''statements = []
rotation = False
postcode = 
random = False
childs = []
typ = False
cafeteria = []
hide = False
dontknow = False
id = B0
precode = 
size = []
parent_id = False
content = False'''.splitlines())
        self.assertEqual(expected, result)

if __name__ == '__main__':
    main()