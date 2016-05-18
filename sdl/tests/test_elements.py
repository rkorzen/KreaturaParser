# from unittest import TestCase
from lxml import etree
from sdl.tools import KreaturaTestCase, find_by_id, make_caf_to_dim
from sdl.kparser import parse
from sdl.elements import Survey, Block, Page, Question, Control, ScriptsCalls, Row, Cell
from sdl.elements import ControlLayout, ControlOpen, ControlSingle,ControlMulti, Cafeteria, ControlNumber, ControlTable


class TestSurvey(KreaturaTestCase):
    def test_append(self):
        surv1 = Survey()
        surv1.childs.append('A')

        surv2 = Survey()
        surv2.append('A')

        self.assertEqual(surv1, surv2)

    def test_add_to_parent(self):
        """Uzycie metody add_to_parent powinno dać ten sam efekt, co ręczne dodawanie"""

        surv = Survey()
        b1, b2, b3 = Block('B1'), Block('B2'), Block('B3')
        b3.parent_id = 'B2'

        surv.append(b1)
        b1.childs.append(b2)
        surv.add_to_parent(b3)

        e_surv = Survey()
        e_b1, e_b2, e_b3 = Block('B1'), Block('B2'), Block('B3')
        e_b3.parent_id = "B2"

        e_surv.append(e_b1)
        e_b1.childs.append(e_b2)
        e_b2.childs.append(e_b3)

        self.assertEqual(surv, e_surv)

    def test_survey_attributes(self):
        """Pusty element Survey ma trochę atrybutów stałych (domyślnych) i jeden zmienny (createtime)"""
        got = Survey()
        epoch_time = got.createtime
        got.to_xml()
        got = etree.tostring(got.xml)
        want = ('''<survey SMSComp="false"
                           createtime="{}"
                           creator="CHANGEIT"
                           exitpage=""
                           layoutid="ShadesOfGray"
                           localeCode="pl"
                           name="CHANGEIT"
                           sensitive="false"
                           showbar="false"
                           time="60000">
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                   </survey>'''.format(epoch_time))

        self.assertXmlEqual(got, want)

    def test_build_xml(self):
        """Metoda to_xml wywoływana jest takż na dzieciach

        Tak naprawdę to ten test trreba by umieścić w innym miejscu
        """

        surv = Survey()
        epoch_time = surv.createtime  # czesc zmienna - musze wstawic ten czas do expected

        # Dodajemmy 2 zagnieżdzone bloki. Blok B1 zawiera B2
        surv.append(Block('B1'))
        surv.childs[0].childs.append(Block('B2'))

        surv.to_xml()
        xml_expc = etree.fromstring('''<survey SMSComp="false"
                           createtime="{}"
                           creator="CHANGEIT"
                           exitpage=""
                           layoutid="ShadesOfGray"
                           localeCode="pl"
                           name="CHANGEIT"
                           sensitive="false"
                           showbar="false"
                           time="60000">
                           <block id="B1" name="" quoted="false" random="false" rotation="false">
                           <block id="B2" name="" quoted="false" random="false" rotation="false"/>
                           </block>
                           <vars></vars>
                           <procedures>
                            <procedure id="PROC" shortdesc=""></procedure>
                           </procedures>
</survey>'''.format(epoch_time))
        self.assertXmlEqual(etree.tostring(surv.xml), etree.tostring(xml_expc))


class TestBlock(KreaturaTestCase):

    def test_class_exist(self):
        b = Block('B1')
        self.assertIsInstance(b, Block)

    def test_class_init(self):
        b = Block('B1')
        self.assertEqual('B1', b.id)

    def test_build_xml(self):
        e_xml = etree.tostring(etree.fromstring('<block id="B1" name="" quoted="false" random="false" rotation="false">'
                                                '<block id="B2" name="" quoted="false" random="false" rotation="false">'
                                                '</block></block>'))
        b1 = Block('B1')
        b2 = Block('B2')
        b1.childs.append(b2)
        b1.to_xml()

        xml = etree.tostring(b1.xml)
        self.assertEqual(e_xml, xml)

    def test_quoted(self):
        b = Block('B1')
        b.quoted = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="true" random="false" rotation="false"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)

    def test_random(self):
        b = Block('B1')
        b.random = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="false" random="true" rotation="false"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)

    def test_rotation(self):
        b = Block('B1')
        b.rotation = True

        b.to_xml()

        want = '<block id="B1" name="" quoted="false" random="false" rotation="true"></block>'

        self.assertXmlEqual(etree.tostring(b.xml), want)


class TestPage(KreaturaTestCase):

    def test_class_exist(self):
        p = Page('P1')
        self.assertIsInstance(p, Page)

    def test_class_init(self):
        p = Page('P1')
        self.assertEqual('P1', p.id)

    def test_build_xml(self):
        e_xml = etree.tostring(etree.fromstring('<page id="P1" hideBackButton="false" name=""></page>'))
        p = Page('P1')

        p.to_xml()

        xml = etree.tostring(p.xml)
        self.assertEqual(e_xml, xml)


class TestQuestion(KreaturaTestCase):
    def test_to_xml(self):
        question = Question('Q1')
        question.content = ""
        question.to_xml()

        result = etree.tostring(question.xml, pretty_print=True)
        expected = """  <question id="Q1" name="">
    <control_layout id="Q1.labelka" layout="default" style="">
      <content></content>
    </control_layout>
  </question>"""
        # expected = etree.tostring(expected, pretty_print=True)

        self.assertXmlEqual(result, expected)


class TestToDim(KreaturaTestCase):
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
        input_ = """Q S Q1 COS--list:MARKI
    A
    B
    C
    """
        expected = """
    MARKI - define
    {
        x1 "A",
        x2 "B",
        x3 "C"

    };

    Q1 "COS"
    Categorical [1..1]
    {
        use MARKI -
    };
"""

        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out

        self.assertTxtEqual(result, expected)

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
        input_ = """Q S Q1 COS
    --use:MARKI
    """
        expected = """
    Q1 "COS"
    Categorical [1..1]
    {
        use MARKI -

    };
"""
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out

        self.assertTxtEqual(expected, result)

    def test_use_defined_list_and_other(self):
        input_ = """Q S Q1 COS
    --use:MARKI
    98.d Don't know
    """
        expected = """
    Q1 "COS"
    Categorical [1..1]
    {
        use MARKI -,
        - "Don't know" DK

    };
"""
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out

        self.assertTxtEqual(result, expected)

    def test_DnD_buckets_with_image_buttons(self):
        input_ = r"""Q B dndBucketsImage How familiar you are with each og these brands?<br/>--images
    --use:BE2A_ans_dl
    _
    --use:BRANDS
    """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndBucketsImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Images",
            dropType = "buckets"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use BE2A_ans_dl -

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_buckets_with_text_buttons(self):
        input_ = r"""Q B dndBucketsImage How familiar you are with each og these brands?<br/>
    --use:BE2A_ans_dl
    _
    --use:BRANDS
            """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndBucketsImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Text",
            dropType = "buckets"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use BE2A_ans_dl -

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_scale_with_image_buttons(self):
        input_ = r"""Q LHS dndBucketsImage How familiar you are with each og these brands?<br/>--images
    --use:BRANDS
    _
    -5 Hate it
    -4
    -3
    -2
    -1
    0 Neutral
    1
    2
    3
    4
    5 Love it
    """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndBucketsImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Image",
            colImgType = "LoveHate",
            dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            x1 "-5 Hate it",
            x2 "-4",
            x3 "-3",
            x4 "-2",
            x5 "-1",
            x6 "0 Neutral",
            x7 "1",
            x8 "2",
            x9 "3",
            x10 "4",
            x11 "5 Love it"

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_scale_with_text_buttons(self):
        input_ = r"""Q LHS dndLoveHateScaleImage How familiar you are with each og these brands?<br/>
            --use:BRANDS
            _
            -5 Hate it
            -4
            -3
            -2
            -1
            0 Neutral
            1
            2
            3
            4
            5 Love it
            """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndLoveHateScaleImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Text",
            colImgType = "LoveHate",
            dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            x1 "-5 Hate it",
            x2 "-4",
            x3 "-3",
            x4 "-2",
            x5 "-1",
            x6 "0 Neutral",
            x7 "1",
            x8 "2",
            x9 "3",
            x10 "4",
            x11 "5 Love it"

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_scale_love_hate(self):
        input_ = r"""Q LHS dndLoveHateScaleImage How familiar you are with each og these brands?<br/>--images
    --use:BRANDS
    _
    --use:lovehatescale
            """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndLoveHateScaleImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Image",
            colImgType = "LoveHate",
            dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use lovehatescale -

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_scale_gray(self):
        input_ = r"""Q LHS dndScaleTextGray How familiar you are with each og these brands?<br/>--gray
    --use:BRANDS
    _
    --use:lovehatescale
    """
        survey = parse(input_)
        survey.to_dim()
        result = survey.dim_out
        expected = """
    dndScaleTextGray "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop",
            toolPath = "[%ImageCacheBase%]/images/mbtools/",
            rowBtnType = "Text",
            colImgType = "Gray",
            dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use lovehatescale -

        };
    ) expand grid;
"""

        self.assertTxtEqual(result, expected)

    def test_DnD_buckets_exclude(self):
        self.fail()

    def test_DnD_scale_exclude(self):
        self.fail()

    def test_multi_to_dim(self):
        self.maxDiff = None
        input_ = """Q M Q4 W jakiej wielkości miejscowości mieszkasz?
    1 wieś
    2 miasto do 20 tys. mieszkańców
    3 miasto 20.000-49.999 mieszkańców
    4 miasto 50.000-99.999 mieszkańców
    5 miasto 100.000-199.999 mieszkańców
    6 miasto 200.000-499.999 mieszkańców
    7 miasto 500.000 mieszkańców lub większe
    8 nie wiem/ trudno powiedzieć"""

        survey = parse(input_)
        survey.to_dim()
        got = survey.dim_out
        want = '''
    Q4 "W jakiej wielkości miejscowości mieszkasz?"
    Categorical [1..]
    {
        x1 "wieś",
        x2 "miasto do 20 tys. mieszkańców",
        x3 "miasto 20.000-49.999 mieszkańców",
        x4 "miasto 50.000-99.999 mieszkańców",
        x5 "miasto 100.000-199.999 mieszkańców",
        x6 "miasto 200.000-499.999 mieszkańców",
        x7 "miasto 500.000 mieszkańców lub większe",
        x8 "nie wiem/ trudno powiedzieć"

    };
'''
        self.assertTxtEqual(got, want)


class TestToWeb(KreaturaTestCase):

    # region block tests
    def test_precode(self):
        text_input = """Q S Q1 COS
PRE ' xxx
1 a
2 b"""
        survey = parse(text_input)
        survey.to_web()
        result = survey.web_out

        expected = "    ' xxx\n    Q1.Ask()\n"

        self.assertEqual(expected, result)


    def test_postcode(self):
        text_input = """Q S Q1 COS
POST ' xxx
1 a
2 b"""
        survey = parse(text_input)
        x = survey.childs[0].childs[0]
        survey.to_web()
        result = survey.web_out

        expected = "    Q1.Ask()\n    ' xxx\n"

        self.assertEqual(expected, result)


class TestQuestionSpecialMarkers(KreaturaTestCase):

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


class TestControl(KreaturaTestCase):

    def test_control(self):
        c = Control('id')
        self.assertIsInstance(c, Control)
        self.assertEqual(c.id, 'id')


class TestControlLaout(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlLayout('Q1')
        c.to_xml()
        result = etree.tostring(c.xml, pretty_print=True)

        expected = etree.fromstring('<control_layout id="Q1" layout="default" style=""><content/></control_layout>')
        expected = etree.tostring(expected, pretty_print=True)

        self.assertXmlEqual(expected, result)

    def test_content_in_kwargs(self):
        c = ControlLayout('Q1', **{'content': 'COS'})
        c.to_xml()
        want = '<control_layout id="Q1" layout="default" style=""><content>COS</content></control_layout>'
        got = etree.tostring(c.xml)

        self.assertXmlEqual(got, want)


class TestControlOpen(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlOpen('Q1')
        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_open id="Q1" length="25" lines="1" mask=".*" name="Q1"
require="true" results="true" style=""><content/></control_open>'''

        self.assertXmlEqual(got, want)


class TestControlSingle(KreaturaTestCase):
    def test_to_xml(self):
        single = ControlSingle('Q1')
        caf = Cafeteria()
        caf.id = '1'
        caf.content = "A"
        single.cafeteria = [caf]

        single.name = "test"
        single.to_xml()
        got = etree.tostring(single.xml)
        want = '''<control_single id="Q1" itemlimit="0" layout="vertical" name="test" random="false" require="true"
        results="true" rotation="false" style=""><list_item id="1" name="" style=""><content>A</content></list_item>
        </control_single>'''

        self.assertXmlEqual(got, want)

    def test_wartosci_nadpisane(self):
        single = ControlSingle('Q1', **{"random": 'true'})
        single.name = 'Q1 COS'

        caf = Cafeteria()
        caf.id = "1"
        caf.content = "a"

        single.cafeteria = [caf]

        single.to_xml()
        want = '<control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 COS" random="true" ' \
               'require="true" results="true" rotation="false"><list_item id="1" name="" style="">' \
               '<content>a</content></list_item></control_single>'
        got = etree.tostring(single.xml)

        self.assertXmlEqual(got, want)

    def test_no_cafeteria(self):
        single = ControlSingle('Q1', **{"random": 'true'})
        single.name = 'Q1 COS'
        self.assertRaises(ValueError, single.to_xml)

    def test_with_i(self):
        single = ControlSingle('Q1')
        caf = Cafeteria()
        caf.id = '1'
        caf.content = "A--i"
        single.cafeteria = [caf]

        single.name = "test"
        single.to_xml()
        got = etree.tostring(single.xml)
        want = '''<control_single id="Q1" itemlimit="0" layout="vertical" name="test" random="false" require="true"
        results="true" rotation="false" style=""><list_item id="1" name="" style=""><content>&lt;i&gt;A&lt;/i&gt;</content></list_item>
        </control_single>'''
        self.assertXmlEqual(got, want)


class TestControlMulti(KreaturaTestCase):
    def test_to_xml(self):
        single = ControlMulti('Q1')
        caf = Cafeteria()
        caf.id = '1'
        caf.content = "A"
        single.cafeteria = [caf]

        single.name = "test"
        single.to_xml()
        got = etree.tostring(single.xml)
        want = '''<control_multi id="Q1" itemlimit="0" layout="vertical" name="test" random="false" require="true"
        results="true" rotation="false" style=""><list_item id="1" name="" style=""><content>A</content></list_item>
        </control_multi>'''

        self.assertXmlEqual(got, want)


class TestControlNumber(KreaturaTestCase):
    def test_to_xml(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_max(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.max = "1"
        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" max="1" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_min(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.min = "1"

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" min="1" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)

    def test_maxsize(self):
        c = ControlNumber('Q2')
        c.content = 'test'
        c.name = c.id + ' | ' + c.content
        c.maxsize = "2"

        c.to_xml()
        got = etree.tostring(c.xml)
        want = '''<control_number float="false" id="Q2" mask=".*" maxsize="2" name="Q2 | test" require="true" results="true"
style=""><content/></control_number>'''

        self.assertXmlEqual(got, want)


class TestCafeteria(KreaturaTestCase):
    def test_to_xml(self):
        c = Cafeteria()
        c.id = "1"
        c.content = "A"
        c.hide = '$Q1:{0} == "1"'

        c.to_xml()

        got = etree.tostring(c.xml, pretty_print=True)
        want = '''
<list_item id="1" name="" style="">
<content>A</content>
<hide><![CDATA[$Q1:1 == "1"]]></hide>
</list_item>
'''

        self.assertXmlEqual(got, want)

    def test_repr(self):
        c = Cafeteria()
        c.id = '1'
        c.content = 'a'
        self.assertEqual('1,a', str(c))


class TestScriptsCalls(KreaturaTestCase):
    def setUp(self):
        self.sc = ScriptsCalls('Q1')
        self.want = etree.Element('control_layout')
        self.want.set('id', self.sc.id+'.js')
        self.want.set('layout', 'default')
        self.want.set('style', "")
        self.content = etree.SubElement(self.want, 'content')

    def test_js_table(self):
        # print(self.sc.id)
        # content.text = 'A'

        self.content.text = '''
<!-- tabela js -->
<link rel="stylesheet" href="public/tables.css" type="text/css">
<script type='text/javascript' src='public/tables.js'></script>
<script type='text/javascript'>

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table("{0}_");

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
</script>

<!-- custom css -->
<link rel="stylesheet" href="public/custom.css" type="text/css">
'''.format(self.sc.id)

        self.sc.js_table()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_obrazki_zamiast_kafeterii(self):
        self.content.text = '''
<!-- Obrazki zamiast kafeterii -->
<script type='text/javascript'>
var multiImageControlId = '{0}';
</script>
'''.format(self.sc.id)
        self.sc.obrazki_zamiast_kafeterii()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_list_column(self):
        self.sc.columns = 2

        self.content.text = '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
new IbisListColumn("{0}",{1});
</script>
'''.format(self.sc.id, 2)

        self.sc.list_column()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_list_column_example(self):
        self.sc.columns = 2

        self.content.text = '''
<!-- list column -->
<link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css">
<script type='text/javascript' src='public/listcolumn/listcolumn.js'></script>
<script type='text/javascript'>
  // new IbisListColumn("{0}",{1});
</script>
'''.format(self.sc.id, 2)

        self.sc.list_column(example=True)
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_dezaktywacja_opena(self):
        self.content.text = '''
<!-- dezaktywacja opena -->
<script type='text/javascript'>
    var opendisDest = "{0}";
    var opendisText = "Nie wiem / trudno powiedzieć";
    var opendisValue = "98";
</script>
<script type='text/javascript' src='opendis/opendis.js'></script>
'''.format(self.sc.id)

        self.sc.dezaktywacja_opena()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_superimages(self):
        self.content.text = '''<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.sc.id)

        self.sc.superimages()
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))

    def test_superimages_example(self):
        self.content.text = '''<!-- super images -->
<link rel='stylesheet' type='text/css' href='public/superImages.css'/>
<script type='text/javascript' src='public/superImages.js'></script>
<script type='text/javascript'>
  // s{0} = new SuperImages("{0}", {{zoom: false}});
</script>
'''.format(self.sc.id)

        self.sc.superimages(example=True)
        got = self.sc.to_xml()

        self.assertXmlEqual(etree.tostring(got), etree.tostring(self.want))


class TestRow(KreaturaTestCase):
    def setUp(self):
        self.row = Row()

    def test_row(self):
        self.assertEqual(self.row.cells, [])
        self.assertEqual(self.row.forcestable, 'true')
        self.assertEqual(self.row.style, '')
        self.assertEqual(self.row.xml, None)


    def test_add_cell_error(self):
        self.assertRaises(TypeError, self.row.add_cell, 'cos')


    def test_add_cell(self):
        cell = Cell()
        self.row.add_cell(cell)
        self.assertEqual(self.row.cells, [cell])


    def test_to_xml(self):
        cell = Cell()
        cl = ControlLayout('Q1')
        cell.add_control(cl)

        self.row.add_cell(cell)
        self.row.to_xml()

        want = """<row forcestable='true' style=''><cell colspan='1' forcestable='false' rowspan='1' style=''>
        <control_layout id='Q1' layout="default" style=""><content></content></control_layout></cell></row>"""
        got = etree.tostring(self.row.xml)

        self.assertXmlEqual(got, want)


class TestCell(KreaturaTestCase):
    def setUp(self):
        self.cell = Cell()

    def test_cell(self):
        self.assertIsInstance(self.cell, Cell)
        self.assertEqual(self.cell.colspan,"1")
        self.assertEqual(self.cell.forcestable, "false")
        self.assertEqual(self.cell.rowspan, "1")
        self.assertEqual(self.cell.style, "")
        self.assertEqual(self.cell.xml, None)
        self.assertEqual(self.cell.control, None)

    def test_add_control_real(self):
        control = ControlLayout("Q1")
        self.cell.add_control(control)
        self.assertIsInstance(self.cell.control, ControlLayout)
        self.assertEqual(self.cell.control.id, "Q1")

    def test_to_xml(self):
        control = ControlLayout("Q1")
        self.cell.add_control(control)
        self.cell.to_xml()
        result = etree.tostring(self.cell.xml, pretty_print=True)
        expected = """<cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_layout id="Q1" layout="default" style="">
        <content/>
    </control_layout>
</cell>"""

        self.assertXmlEqual(result, expected)


    def test_to_xml_without_cell(self):
        cell = Cell()
        self.assertRaises(ValueError, cell.to_xml)


    def test_add_control_without_to_xml(self):
        cell = Cell()
        cell.add_control('Kontrolka')
        self.assertRaises(AttributeError, cell.to_xml)


class TestControlTable(KreaturaTestCase):
    def setUp(self):
        self.table = ControlTable('T1')

    def test_table(self):
        """<control_table id="A5_table" random="false" rotation="false" rrdest="row" style="">"""
        self.assertEqual(self.table.id, 'T1')
        self.assertEqual(self.table.random, 'false')
        self.assertEqual(self.table.rotation, 'false')
        self.assertEqual(self.table.rrdest, 'row')
        self.assertEqual(self.table.style, '')
        self.assertEqual(self.table.rows, [])
        self.assertEqual(self.table.xml, None)

    def test_add_row(self):
        row = Row()
        self.table.add_row(row)
        self.assertEqual(self.table.rows, [row])

    def test_add_row_and_there_is_no_row_instance(self):
        row = "row"
        self.assertRaises(TypeError, self.table.add_row, row)

    def test_to_xml(self):
        want = """<control_table id="T1" random='false' rotation='false' rrdest='row' style=''><row forcestable='true'
         style=''><cell colspan='1' forcestable='false' rowspan='1' style=''><control_layout id='Q1' layout="default"
         style=""><content></content></control_layout></cell></row></control_table>"""

        cl = ControlLayout('Q1')
        cell = Cell()
        row = Row()

        cell.add_control(cl)
        row.add_cell(cell)

        self.table.add_row(row)
        self.table.to_xml()

        got = etree.tostring(self.table.xml)
        self.assertXmlEqual(got, want)

    def test_to_xml_no_row(self):
        self.assertRaises(ValueError, self.table.to_xml)

    def test_to_xml_no_cell_on_row(self):
        row = Row()
        self.table.add_row(row)
        self.assertRaises(ValueError, self.table.to_xml)


if __name__ == '__main__':
    KreaturaTestCase.main()