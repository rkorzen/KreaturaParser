from unittest import main
from KreaturaParser.kparser import parse, print_tree
from KreaturaParser.elements import Block, Page, Question, Cafeteria, Survey
from lxml import etree
from KreaturaParser.tests.testing_tools import KreaturaTestCase
# from KreaturaParser.tools import show_attr


class TestParse(KreaturaTestCase):

    # region block tests
    def test_grid_with_categories_loop(self):
        text_input = """Q G Q1 COS
1 odp a
2 odp b
_
1 stw a {@}
2 stw b {@}

FOR CATEGORIES:
1 cat 1
2 cat 2"""
        survey = parse(text_input)
        survey.to_dim()
        result = survey.dim_out

        expected = """
    Q1 - loop
    {
        c1 "cat 1",
        c2 "cat 2"

    } ran fields -
    (
        LR " COS" loop
        {
            l1 "stw a {@}",
            l2 "stw b {@}"

        } fields -
        (
            slice ""
            categorical [1..1]
            {
                x1 "odp a",
                x2 "odp b"

            };
        ) expand grid;
    ) expand;
"""

        self.assertEqual(expected, result)

    def test_wersjonowanie(self):
        text_input = """Q S Q1 Czy może Pan(i)  powiedzieć, o co Panu(i) chodzi
1 chętny/a
2 niechętny(a)
"""
        survey = parse(text_input)
        survey.to_dim()
        result = survey.dim_out
        print(result)

    def test_control_single_with_i(self):
        text_input = """Q S Q1 COS
1 odp a --i
2 odp b
"""
        survey = parse(text_input)
        survey.to_dim()
        result = survey.dim_out
        print(result)
        expected = """
    Q1 "COS"
    Categorical [1..1]
    {
        x1 "<i>odp a</i>",
        x2 "odp b"

    };
"""
        self.assertEqual(result, expected)

    def test_img_caf(self):
        input_ = """Q S Q1 COS
A|1.jpg
B|c\\2.jpg
"""
        expected = r'''
    Q1 "COS"
    Categorical [1..1]
    {
        x1 "A"
            labelstyle(
                Image = "images\1.jpg",
                ImagePosition = "ImageOnly"
            ),
        x2 "B"
            labelstyle(
                Image = "images\c\2.jpg",
                ImagePosition = "ImageOnly"
            )1

    };
'''
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        #self.assertMultiLineEqual(result, expected)
        self.assertTxtEqual(result, expected)

    def test_przyklad(self):
        A = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Proin venenatis libero ante, in posuere felis  egestas vel.
Vivamus tristique et mi eget convallis. Vestibulum id quam porta, semper leo quis, finibus orci.
Pellentesque vel sapien elementum, iaculis diam in,  fringilla nisi. Morbi interdum luctus dolor sit amet euismod.
Donec in rhoncus purus, ac venenatis justo. Nulla ac purus ut tortor molestie facilisis sed sit amet tellus.
Vivamus consequat risus vel  consequat rhoncus.
"""
        B = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Proin venenatis libero ante, in posuere felis egestas vel.
Vivamus tristique et mi eget convallis. Vestibulum id quam porta, semper leo quis, finibus orci.
Pellentesque vel sapien elementum, iaculis diam in, fringilla nisi. Morbi interdum luctus dolor sit amet euismod.
Donec in rhoncus purus, ac venenatis justo. Nulla ac purus ut tortor molestie facilisis sed sit amet tellus.
Vivamus consequat risus vel consequat rhoncus.
"""
        #self.assertMultiLineEqual(A, B)
        self.assertTxtEqual(A, B)

    def test_grid_by_slice(self):
        self.fail()