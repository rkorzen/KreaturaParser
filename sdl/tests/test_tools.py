from lxml import etree
from sdl.tools  import KreaturaTestCase
from sdl.kparser import parse
from sdl.elements import Cafeteria
from sdl.tools import show_attr, find_parent, find_by_id, build_precode, clean_labels, wersjonowanie_plci, filter_parser
from sdl.tools import clean_line, print_tree, make_caf_to_dim


class Test(object):
    pass


class SomeObject:
    def __init__(self):
        self.x = 'x'
        self.y = 'y'


class TestShowAttr(KreaturaTestCase):
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

    def test_block_show_attr(self):
        from sdl.kparser import parse
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
categories = []
hide = False
dontknow = None
id = B0
precode = False
size = []
parent_id = False
content = False
dim_out = ""
spss_out = ""
xml = None
quoted = False
web_out = ""
warnings = []
kwargs = {}
'''.splitlines())

        self.assertEqual(expected, result)

    def test_print_attr(self):
        element = SomeObject()
        result = show_attr(element)
        expected = sorted('x = x\ny = y'.splitlines())
        self.assertEqual(expected, result)


class TestFindParrent(KreaturaTestCase):
    def test_find_parrent(self):
        input_ = """B B0
B B2
P P2

P P1
Q S Q1 A

B B3
"""
        survey = parse(input_)
        self.assertEquals("P1", find_parent(survey, "Q1"))
        self.assertEquals("B2", find_parent(survey, "P2"))

class TestFindById(KreaturaTestCase):
    def test_find_by_id(self):
        input_ = """B B0
B B2
P P2

P P1
Q S Q1 A

"""
        survey = parse(input_)
        qr = find_by_id(survey, 'Q1')

        self.assertEqual(qr.id, "Q1")
        self.assertEqual(qr.typ, "S")
        self.assertEqual(qr.content, "A")


class TestBuildPrecode(KreaturaTestCase):

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


class TestCleanLabels(KreaturaTestCase):
    def test_clean_labels_img(self):
        in_ = '''<img src='public/koncept_1.jpg' alt="koncept_1">koncept 1<br> <span style="color:red">cos</span>'''
        want = 'koncept 1 cos'
        got = clean_labels(in_)
        self.assertEqual(got, want)


class TestWersjonowaniePlci(KreaturaTestCase):
    def test_wersjonowanie_plci(self):
        in_ = 'Pan(i) Pana(i) Panem(nią)'
        got = wersjonowanie_plci(in_)
        want = '#SEX_M# #SEX_D# #SEX_N#'
        self.assertEqual(got, want)


    def test_wersjonowanie_plci_dim(self):
        in_ = 'Pan(i) Pana(i) Panem(nią)'
        got = wersjonowanie_plci(in_, "dim")
        want = '{#Pan} {#Pana} {#Panem}'
        self.assertEqual(got, want)


class TestFilter_parser(KreaturaTestCase):
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
        expected = "    ' if cos the cos"
        self.assertEqual(expected, result)


class TestCleanLine(KreaturaTestCase):

    def test_double_spaces(self):
        line = "B  B0  "
        self.assertEqual('B B0', clean_line(line))

    def test_tabulation_spaces(self):
        line = "B\tB0  "
        self.assertEqual('B B0', clean_line(line))

    def test_ampersand(self):
        line = "Q S Q1 Procter & gamble  "
        self.assertEqual('Q S Q1 Procter &amp; gamble', clean_line(line))

    def test_switch_with_spaces(self):
        line = "_  "
        self.assertEqual("_", clean_line(line))


class TestPrintTree(KreaturaTestCase):
    def test_print_tree(self):
        input_ = """B B0
B B1 B0
B B2 B0
P P1
Q S Q1 cos
B B3 B2
B B4"""

        survey = parse(input_)
        result = print_tree(survey)
        expected = '''B0
\tB1
\tB2
\t\tP1
\t\t\tQ1
\t\tB3
B4'''
        self.assertEqual(expected, result)

    def test_print_tree_2(self):
        input_ = """B B0

B B1 B0

B B2 B0

P P1

Q S Q1 cos

B B3 B2

B B4"""

        survey = parse(input_)
        result = print_tree(survey)
        expected = '''B0
\tB1
\tB2
\t\tP1
\t\t\tQ1
\t\tB3
B4'''
        self.assertEqual(expected, result)


class TestMakeCafeteriaToDim(KreaturaTestCase):

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


if __name__ == '__main__':
    KreaturaTestCase.main()