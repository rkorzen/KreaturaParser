from lxml import etree
from KreaturaParser.kparser import parse, print_tree
from KreaturaParser.tools import KreaturaTestCase, find_by_id

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

        self.assertTxtEqual(expected, result)

    def test_wersjonowanie(self):
        text_input = """Q S Q1 Czy może Pan(i)  powiedzieć, o co Panu(i) chodzi
1 chętny/a
2 niechętny(a)
"""
        survey = parse(text_input)
        survey.to_dim()
        result = survey.dim_out

        expected = '''
    Q1 "Czy może {#Pan}  powiedzieć, o co {#Panu} chodzi"
    Categorical [1..1]
    {
        x1 "chętn{#y}",
        x2 "niechętn{#y}"

    };
'''
        self.assertTxtEqual(expected, result)

    def test_control_single_with_i(self):
        text_input = """Q S Q1 COS
1 odp a --i
2 odp b
"""
        survey = parse(text_input)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    Q1 "COS"
    Categorical [1..1]
    {
        x1 "<i>odp a</i>",
        x2 "odp b"

    };
"""
        self.assertTxtEqual(result, expected)

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
            )

    };
'''
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        self.assertTxtEqual(result, expected)

    def test_define_and_use_list(self):
        input_ = """Q S Q1 COS --list:MARKI
A
B
C
"""
        expected = """
    MARKI "" define
    {
        _1 "A",
        _2 "B",
        _3 "C"
    };

    Q1 "COS"
    Categorical [1..1]
    {
        MARKI use \\.MARKI -
    };
"""

        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out

        self.assertTxtEqual(expected, result)

    def test_define_list_wrong_format(self):
        input_ = "Q S Q1 COS --list: coś\na\nb"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_dim)

    def test_use_list_wrong_format(self):
        input_ = "Q S Q1 COS --use: coś\na\nb"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_dim)

    def test_use_marker_and_list_marker_together(self):
        input_ = "Q S Q1 COS --use:MARKA--list:MARKA2"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_dim)

    def test_dim_create_list(self):
        input_ = "Q S Q1 COS list:MARKI\na\nb"
        survey = parse(input_)
        question = find_by_id(survey, 'Q1')
        x = question.dim_create_list("MARKI")
        expected = '''
    MARKI - define
    {
        x1 "a",
        x2 "b"

    };
'''
        self.assertTxtEqual(x, expected)

    def test_use_defined_list(self):
        input_ = """Q S Q1 COS --list:MARKI
        --use:MARKI
"""
        expected = """
    Q1 "COS"
    Categorical [1..1]
    {
        MARKI use \\.MARKI -
    };
"""
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out

        self.assertEqual(expected, result)

    def test_DnD_buckets_with_image_buttons(self):
        self.fail()

    def test_DnD_buckets_with_text_buttons(self):
        self.fail()

    def test_DnD_scale_with_image_buttons(self):
        self.fail()

    def test_DnD_scale_with_text_buttons(self):
        self.fail()

    def test_DnD_scale_love_hate(self):
        self.fail()

    def test_DnD_scale_gray(self):
        self.fail()

    def test_DnD_buckets_exclude(self):
        self.fail()

    def test_DnD_scale_exclude(self):
        self.fail()

class TestSpecialMarkers(KreaturaTestCase):

    def test_minchoose_ibis(self):
        input_ = "Q M Q1 COS --minchoose:4\na\nb"
        survey = parse(input_)
        survey.to_xml()
        expected = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>COS </content>
        </control_layout>
        <control_multi id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS " random="false" require="true" results="true" rotation="false" minchoose="4">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>b</content>
          </list_item>
        </control_multi>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>""".format(survey.createtime)

        result = etree.tostring(survey.xml, pretty_print=True)
        self.assertXmlEqual(result, expected)

    def test_maxchoose_ibis(self):
        input_ = "Q M Q1 COS --maxchoose:4\na\nb"
        survey = parse(input_)
        survey.to_xml()
        expected = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>COS </content>
        </control_layout>
        <control_multi id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS " random="false" require="true" results="true" rotation="false" maxchoose="4">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>b</content>
          </list_item>
        </control_multi>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>""".format(survey.createtime)

        result = etree.tostring(survey.xml, pretty_print=True)
        self.assertXmlEqual(result, expected)

    def test_minchoose_dim(self):
        input_ = "Q M Q1 COS --minchoose:4\na\nb\nc\nd\ne"
        survey = parse(input_)
        survey.to_dim()
        expected = """
    Q1 "COS "
    Categorical [4..]
    {
        x1 "a",
        x2 "b",
        x3 "c",
        x4 "d",
        x5 "e"

    };
"""
        self.assertTxtEqual(expected, survey.dim_out)

    def test_maxchoose_dim(self):
        input_ = "Q M Q1 COS --maxchoose:4\na\nb\nc\nd\ne"
        survey = parse(input_)
        survey.to_dim()
        expected = """
    Q1 "COS "
    Categorical [1..4]
    {
        x1 "a",
        x2 "b",
        x3 "c",
        x4 "d",
        x5 "e"

    };
"""
        self.assertTxtEqual(expected, survey.dim_out)


    def test_minchoose_error(self):
        input_ = "Q S Q1 COS --minchoose:x\na\nb"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_dim)


    def test_maxchoose_error(self):
        input_ = "Q S Q1 COS --maxchoose:x\na\nb"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_dim)

