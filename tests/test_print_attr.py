from unittest import TestCase, main
from KreaturaParser.tools import show_attr


class SomeObject:
    def __init__(self):
        self.x = 'x'
        self.y = 'y'


class TestPrintAttr(TestCase):
    def test_print_attr(self):
        element = SomeObject()
        result = show_attr(element)
        expected = sorted('x = x\ny = y'.splitlines())

        self.assertEqual(expected, result)

    def test_block(self):
        from KreaturaParser.kparser import parse
        input_ = 'B B0'
        survey = parse(input_)
        b = survey.childs[0]
        result = show_attr(b)

        # zmiana postcode - z false na ""
        expected = sorted('''statements = []
rotation = False
postcode = False
random = False
childs = []
typ = False
cafeteria = []
hide = False
dontknow = None
id = B0
precode = False
size = []
parent_id = False
content = False
dim_out = ""
xml = None
quoted = False
warnings = []'''.splitlines())

        self.assertEqual(expected, result)


if __name__ == '__main__':
    main()
