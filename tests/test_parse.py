from unittest import main
from kparser import parse
from elements import Block, Page, Question, Cafeteria, Survey
from lxml import etree
from tests.testing_tools import KreaturaTestCase


class TestParse(KreaturaTestCase):

    # region block tests
    def test_block(self):
        text_input = """B B0"""
        result = parse(text_input)
        block = Block("B0")
        survey = Survey()
        survey.append(block)
        expected = survey
        self.assertEqual(expected, result)

    def test_block_page(self):
        text_input = """B B0
P P0"""
        result = parse(text_input)
        block = Block("B0")
        page = Page("P0")
        block.childs.append(page)
        survey = Survey()
        survey.append(block)
        expected = survey

        self.assertEqual(expected, result)

    def test_block_question(self):
        text_input = """B B0
Q S Q1 Cos"""
        block = Block("B0")
        page = Page("Q1_p")
        question = Question("Q1")
        question.typ = "S"
        question.content = "Cos"
        page.childs.append(question)
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_block_precode_postcode(self):
        text_input = "B B0\nPRE x\nPOST y"
        block = Block("B0")
        block.precode = "x"
        block.postcode = "y"

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_block_parrent(self):
        input_ = """B B0

B B1 B0
"""
        b1 = Block('B0')
        b2 = Block('B1')

        b2.parent_id = "B0"

        b1.childs.append(b2)

        survey = Survey()
        survey.append(b1)
        expected = survey

        result = parse(input_)
        self.assertEqual(expected, result)
    # endregion

    # region page tests
    def test_page(self):
        text_input = "P P0"
        page = Page("P0")
        block = Block("Default")
        block.childs.append(page)
        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_page_question(self):
        text_input = "P P0\nQ S Q1 tresc"

        question = Question('Q1')
        question.typ = "S"
        question.content = "tresc"

        page = Page("P0")
        page.childs.append(question)

        block = Block("Default")
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)

        self.assertEqual(expected, result)

    def test_page_precode_postcode(self):
        text_input = "P P0\nPRE x\nPOST y"
        page = Page("P0")
        page.precode = "x"
        page.postcode = "y"

        block = Block("Default")
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)
    # endregion

    # region question test
    def test_question(self):
        text_input = "Q S Q0 pytanie"

        question = Question('Q0')
        question.typ = "S"
        question.content = "pytanie"

        page = Page("Q0_p")
        page.childs.append(question)

        block = Block("Default")
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_question_rot(self):
        input_ = "Q S Q1 Cos --rot"
        question = Question('Q1')
        question.typ = 'S'
        question.content = 'Cos'
        question.rotation = True

        page = Page('Q1_p')
        page.childs.append(question)

        blok = Block('Default')
        blok.childs.append(page)

        survey = Survey()
        survey.append(blok)

        result = parse(input_)

        self.assertEqual(survey, result)

    def test_question_precode_postcode(self):
        text_input = "Q O Q0 Cos\nPRE x\nPOST y"
        question = Question('Q0')
        question.typ = "O"
        question.content = "Cos"
        page = Page("Q0_p")
        page.precode = "x"
        page.postcode = "y"
        page.childs.append(question)
        block = Block("Default")
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)

        self.assertEqual(expected, result)

    def test_two_questions(self):
        text_in = """
Q L Q1 Pyt 1

Q L Q2 Pyt 2

"""
        q1 = Question("Q1")
        q2 = Question("Q2")

        q1.typ = "L"
        q2.typ = "L"

        q1.content = "Pyt 1"
        q2.content = "Pyt 2"

        p1, p2 = Page("Q1_p"), Page("Q2_p")
        block = Block("Default")

        p1.childs.append(q1)
        p2.childs.append(q2)

        block.childs.append(p1)
        block.childs.append(p2)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_in)

        self.assertEqual(expected, result)

    def test_autonum(self):
        input_ = 'Q S Q1 COS\na\nb'
        survey = Survey()

        b = Block('Default')
        survey.append(b)

        p = Page('Q1_p')
        b.childs.append(p)

        q = Question('Q1')
        q.typ = 'S'
        q.content = 'COS'
        p.childs.append(q)

        c1, c2 = Cafeteria(), Cafeteria()
        c1.content = 'a'
        c1.id = '1'
        c2.content = 'b'
        c2.id = '2'

        q.cafeteria.append(c1)
        q.cafeteria.append(c2)

        self.assertEqual(survey, parse(input_))

    def test_numeration_explicite(self):
        input_ = 'Q S Q1 COS\n3 a\n4 b'
        survey = Survey()

        b = Block('Default')
        survey.append(b)

        p = Page('Q1_p')
        b.childs.append(p)

        q = Question('Q1')
        q.typ = 'S'
        q.content = 'COS'
        p.childs.append(q)

        c1, c2 = Cafeteria(), Cafeteria()
        c1.content = 'a'
        c1.id = '3'
        c2.content = 'b'
        c2.id = '4'

        q.cafeteria.append(c1)
        q.cafeteria.append(c2)

        self.assertEqual(survey, parse(input_))

    def test_same_numbers_and_content(self):
        input_ = 'Q S Q1 COS\n1 1\n2 2'
        survey = Survey()

        b = Block('Default')
        survey.append(b)

        p = Page('Q1_p')
        b.childs.append(p)

        q = Question('Q1')
        q.typ = 'S'
        q.content = 'COS'
        p.childs.append(q)

        c1, c2 = Cafeteria(), Cafeteria()
        c1.content = '1'
        c1.id = '1'
        c2.content = '2'
        c2.id = '2'

        q.cafeteria.append(c1)
        q.cafeteria.append(c2)

        self.assertEqual(survey, parse(input_))

    # endregion

    # region BEGIN PROGRAM tests
    def test_empty_program(self):
        input_ = """
B B0
BEGIN PROGRAM
END PROGRAM
"""
        block = Block('B0')

        survey = Survey()
        survey.append(block)
        expected = survey

        self.assertEqual(expected, parse(input_))

    def test_program_loop(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    list = '''Ania
Hania
Lena'''.splitlines()

    out = ""
    for count, person in enumerate(list):
        out += r'''
Q O Q1_{0} Co myślisz o osobie o imieniu {1}
'''.format(count+1, person)
    return out

xxx = func()
END PROGRAM
"""
        block = Block("B0")

        p1 = Page('Q1_1_p')
        p2 = Page('Q1_2_p')
        p3 = Page('Q1_3_p')

        q1 = Question('Q1_1')
        q2 = Question('Q1_2')
        q3 = Question('Q1_3')

        q1.typ = "O"
        q2.typ = "O"
        q3.typ = "O"

        q1.content = "Co myślisz o osobie o imieniu Ania"
        q2.content = "Co myślisz o osobie o imieniu Hania"
        q3.content = "Co myślisz o osobie o imieniu Lena"

        p1.childs.append(q1)
        p2.childs.append(q2)
        p3.childs.append(q3)

        block.childs.append(p1)
        block.childs.append(p2)
        block.childs.append(p3)

        survey = Survey()
        survey.append(block)
        expected = survey

        self.assertEqual(expected, parse(input_))

    def test_block_nesting(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    out = ''
    for i in range(4):
        out += '''B B{1} B{0}
'''.format(i, i+1)
    return out
xxx = func()
END PROGRAM
"""

        b0 = Block("B0")

        b1 = Block("B1")
        b1.parent_id = "B0"

        b2 = Block("B2")
        b2.parent_id = "B1"

        b3 = Block("B3")
        b3.parent_id = "B2"

        b4 = Block("B4")
        b4.parent_id = "B3"

        b0.childs.append(b1)
        b1.childs.append(b2)
        b2.childs.append(b3)
        b3.childs.append(b4)

        survey = Survey()
        survey.append(b0)
        expected = survey
        result = parse(input_)

        self.assertEqual(expected, result)

    def test_block_nesting_one_parent(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    out = ''
    for i in range(4):
        out += '''B B{0} B0

'''.format(i+1)
    return out
xxx = func()
END PROGRAM
"""

        b0 = Block("B0")
        b1 = Block("B1")
        b2 = Block("B2")
        b3 = Block("B3")
        b4 = Block("B4")

        b1.parent_id = "B0"
        b2.parent_id = "B0"
        b3.parent_id = "B0"
        b4.parent_id = "B0"

        b0.childs.append(b1)
        b0.childs.append(b2)
        b0.childs.append(b3)
        b0.childs.append(b4)

        survey = Survey()
        survey.append(b0)
        expected = survey
        result = parse(input_)

        self.assertEqual(expected, result)
    # endregion

    # region question types tests
    def test_single_1_el(self):
        text_input = """B B0
Q S Q1 Cos
1 a"""
        block = Block("B0")
        page = Page("Q1_p")
        question = Question("Q1")
        question.typ = "S"
        question.content = "Cos"
        caf = Cafeteria()
        caf.id = "1"
        caf.content = "a"
        question.cafeteria.append(caf)

        page.childs.append(question)
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_table_1_el_1_st(self):
        text_input = """B B0
Q T Q1 Cos
1 a
_
stwierdzenie 1"""
        block = Block("B0")
        page = Page("Q1_p")
        question = Question("Q1")
        question.typ = "T"
        question.content = "Cos"
        caf = Cafeteria()
        caf.id = "1"
        caf.content = "a"
        question.cafeteria.append(caf)

        stw = Cafeteria()
        stw.content = "stwierdzenie 1"
        stw.id = "1"
        question.statements.append(stw)

        page.childs.append(question)
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)

        self.assertEqual(expected, result)

    def test_open_with_dk_explicite(self):
        line = "Q O Q1 Cos --dk: Nie wiem"
        expected = Survey()
        b = Block('Default')
        p = Page('Q1_p')
        q = Question('Q1')
        q.typ = 'O'
        q.content = 'Cos'
        q.dontknow = 'Nie wiem'
        p.childs.append(q)
        b.childs.append(p)
        expected.append(b)

        result = parse(line)

        self.assertEqual(expected, result)

    def test_open_with_dk_implicite(self):
        line = "Q O Q1 Cos --dk:"
        expected = Survey()
        b = Block('Default')
        p = Page('Q1_p')
        q = Question('Q1')
        q.typ = 'O'
        q.content = 'Cos'
        q.dontknow = 'Nie wiem/trudno powiedzieć'
        p.childs.append(q)
        b.childs.append(p)
        expected.append(b)

        result = parse(line)

        self.assertEqual(expected, result)
    # endregion

    # region Exceptions tests
    def test_wrong_parent_id(self):
        input_ = """B B0
B B1
B B3 B2"""
        self.assertRaises(Exception, parse, input_)
    # endregion

    # region Other
    def test_two_questions_on_page(self):
        input_ = """B B0
P P1

Q O Q1 A

Q O Q2 --p:P1 B
"""
        b1 = Block('B0')
        p1 = Page('P1')

        b1.childs.append(p1)

        q1 = Question('Q1')
        q1.typ = "O"
        q1.content = 'A'

        q2 = Question('Q2')
        q2.typ = "O"
        q2.content = 'B'
        q2.parent_id = "P1"

        p1.childs.append(q1)
        p1.childs.append(q2)

        survey = Survey()
        survey.append(b1)

        result = parse(input_)

        self.assertEqual(survey, result)

    def test_two_questions_parent(self):
        input_ = """Q O Q1 A

Q O Q2 --p:Q1_p COS
"""
        b1 = Block('Default')
        p1 = Page('Q1_p')

        b1.childs.append(p1)

        q1 = Question('Q1')
        q1.typ = "O"
        q1.content = 'A'

        q2 = Question('Q2')
        q2.typ = "O"
        q2.content = 'COS'
        q2.parent_id = "Q1_p"

        p1.childs.append(q1)
        p1.childs.append(q2)

        survey = Survey()
        survey.append(b1)

        result = parse(input_)

        self.assertEqual(survey, result)

    def test_caf_screenout(self):
        input_ = """Q S Q1 A
1 a --so"""

        caf = Cafeteria()
        caf.id = '1'
        caf.content = 'a'
        caf.screenout = True

        q = Question('Q1')
        q.typ = "S"
        q.content = 'A'
        q.cafeteria.append(caf)

        p = Page('Q1_p')
        p.childs.append(q)
        p.postcode = """if ($Q1:1 == "1")
  #OUT = "1"
  goto KONKURS
else
endif"""
        b = Block('Default')
        b.childs.append(p)
        survey = Survey()
        survey.append(b)
        result = parse(input_)
        self.assertEqual(survey, result)
    # endregion


class TestParseToXmlBlock(KreaturaTestCase):
    def test_block_with_precode_to_xml(self):
        input_ = 'B B0\nPRE if($A1:1 == "1");goto next;else;endif'

        result = parse(input_)
        result.to_xml()
        r_xml = etree.tostring(result.xml)

        expected = Survey()
        expected.createtime = result.createtime
        expected.append(Block('B0'))
        expected.childs[0].precode = 'if($A1:1 == "1");goto next;else;endif'
        expected.to_xml()

        e_xml = etree.tostring(expected.xml)
        self.assertEqual(expected, result)
        self.assertXmlEqual(r_xml, e_xml)

    def test_block_precode_value_error(self):
        input_ = 'B B0\nPRE if($A1:1 == "1");goto next;endif'
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_xml)


class TestParseToXmlPage(KreaturaTestCase):
    def test_page_with_precode_to_xml(self):
        input_ = 'P P0\nPRE if($A1:1 == "1");goto next;else;endif'

        result = parse(input_)
        result.to_xml()

        expected = Survey()
        expected.append(Block('Default'))
        expected.childs[0].childs.append(Page('P0'))
        expected.childs[0].childs[0].precode = 'if($A1:1 == "1");goto next;else;endif'
        expected.createtime = result.createtime
        expected.to_xml()

        got = etree.tostring(result.xml)
        want = etree.tostring(expected.xml)
        # print(got,'\n',want)
        self.assertEqual(expected, result)
        self.assertXmlEqual(got, want)

    def test_page_precode_value_error(self):
        input_ = 'P P0\nPRE if($A1:1 == "1");goto next;endif'
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_xml)


class TestParseToXmlOpen(KreaturaTestCase):

    def test_control_open_xml(self):
        line = "Q O Q1 COS"
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_open id="Q1"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1 | COS">
                                                               <content></content>
                                                 </control_open>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_controls_open_xml(self):
        line = """Q O Q1 COS
1 A
8 B"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_open id="Q1_1"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_1 | A">
                                                               <content></content>
                                                 </control_open>
                                                 <control_open id="Q1_8"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_8 | B">
                                                               <content></content>
                                                 </control_open>


                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_controls_open_xml_explicite_id(self):
        line = """Q O Q1 COS
A
B"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_open id="Q1_1"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_1 | A">
                                                               <content></content>
                                                 </control_open>
                                                 <control_open id="Q1_2"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_2 | B">
                                                               <content></content>
                                                 </control_open>


                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_open_size(self):
        line = "Q O90_4 Q1 COS"
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_open id="Q1"
                                                               length="90"
                                                               lines="4"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1 | COS">
                                                               <content></content>
                                                 </control_open>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_open_deactivate(self):
        line = "Q O90_4 Q1 COS --dezaktywacja"
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_open id="Q1"
                                                               length="90"
                                                               lines="4"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1 | COS ">
                                                               <content></content>
                                                 </control_open>
<control_layout id="Q1.js" layout="default" style="">
<content>
&lt;!-- dezaktywacja opena --&gt;
&lt;script type='text/javascript'&gt;
    var opendisDest = "Q1";
    var opendisText = "Nie wiem / trudno powiedzieć";
    var opendisValue = "98";
&lt;/script&gt;
&lt;script type='text/javascript' src='opendis/opendis.js'&gt;&lt;/script&gt;
</content>

</control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)


class TestParseToXmlControlLayout(KreaturaTestCase):
    def test_control_layout_xml(self):
        line = "Q L Q1 COS"
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_controls_layout_xml(self):
        line = """Q L Q1 COS
A
B"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_layout id="Q1_1_txt"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>A</content>
                                                 </control_layout>
                                                 <control_layout id="Q1_2_txt"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>B</content>
                                                 </control_layout>


                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)


class TestParseToXmlControlSingle(KreaturaTestCase):
    def test_control_single_xml(self):
        line = """Q S Q1 COS
A"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_screenout(self):
        line = """Q S Q1 COS
A --so"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 <postcode>
<![CDATA[if ($Q1:1 == "1")
#OUT = "1"
goto KONKURS
else
endif]]></postcode>
                                 </page>
                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_2_screenouts(self):
        line = """Q S Q1 COS
A --so
B --so"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 <postcode>
<![CDATA[if ($Q1:1 == "1")
#OUT = "1"
goto KONKURS
else
endif

if ($Q1:2 == "1")
#OUT = "1"
goto KONKURS
else
endif]]></postcode>
                                 </page>
                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_goto_next(self):
        line = """Q S Q1 COS
A --gn

Q S Q2 COS
A"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
<precode>
<![CDATA[if ($Q1:1 == "1")
    goto next
else
endif]]>
</precode>
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>

                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_goto_next_without_next_page(self):
        line = """Q S Q1 COS
A --gn"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_goto_next_with_block_as_next_el(self):
        line = """Q S Q1 COS
A --gn

B B0
Q L Q2 COS
"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''  <survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
                            localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 | COS" random="false" require="true"
                          results="true" rotation="false" style="">
            <list_item id="1" name="" style="">
              <content>A</content>
            </list_item>
          </control_single>
        </question>
      </page>
    </block>
    <block id="B0" name="" quoted="false" random="false" rotation="false">
        <precode>if ($Q1:1 == &quot;1&quot;)
    goto next
else
endif</precode>
     <page hideBackButton="false" id="Q2_p" name="">
        <question id="Q2" name="">
          <control_layout id="Q2.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
        </question>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def text_control_single_goto_next_without_next_page(self):
        line = """Q S Q1 COS
A --gn"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 <postcode>
<![CDATA[if ($Q1:1 == "1")
#OUT = "1"
goto KONKURS
else
endif

if ($Q1:2 == "1")
#OUT = "1"
goto KONKURS
else
endif]]></postcode>
                                 </page>
                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_single_goto_next_and_screenout(self):
        line = """Q S Q1 COS
A --gn
B --so

Q S Q2 COS
A"""

        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
<postcode>
<![CDATA[if ($Q1:2 == "1")
#OUT = "1"
goto KONKURS
else
endif]]>
</postcode>
                                 </page>
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
<precode>
<![CDATA[if ($Q1:1 == "1")
    goto next
else
endif]]>
</precode>
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>

                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        # etree.tostring(x, pretty_print=True)
        self.assertXmlEqual(got, want)

    def test_control_single_xml_2_goto_next(self):
        line = """Q S Q1 COS
A --gn
B --gn

Q S Q2 COS
A"""

        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
<precode>
<![CDATA[if ($Q1:1 == "1")
    goto next
else
endif

if ($Q1:2 == "1")
    goto next
else
endif]]>
</precode>
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>

                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        # etree.tostring(x, pretty_print=True)
        self.assertXmlEqual(got, want)

    def test_control_single_no_cafeteria(self):
        input_ = "Q S Q1 COS"
        survey = parse(input_)

        self.assertRaises(ValueError, survey.to_xml)

    def test_control_single_caf_with_hide_1_el_caf(self):
        input_ = '''Q S Q2 COS
1 A --hide:$Q1:{0} == "1"'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                    <hide><![CDATA[$Q1:1 == "1"]]></hide>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_control_single_caf_with_hide_2_el_caf(self):
        input_ = '''Q S Q2 COS
1 A --hide:$Q1:{0} == "1"
2 B'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                    <hide><![CDATA[$Q1:1 == "1"]]></hide>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                    <hide><![CDATA[$Q1:2 == "1"]]></hide>
                                                                 </list_item>

                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_control_single_caf_with_hide_change_hide_pattern(self):
        input_ = '''Q S Q2 COS
1 A --hide:$Q1:{0} == "1"
2 B --hide:$Q0:{0} == "1"
3 C'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                    <hide><![CDATA[$Q1:1 == "1"]]></hide>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                    <hide><![CDATA[$Q0:2 == "1"]]></hide>
                                                                 </list_item>
                                                                 <list_item id="3" name="" style="">
                                                                    <content>C</content>
                                                                    <hide><![CDATA[$Q0:3 == "1"]]></hide>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_obrazki_zamiast_kaf(self):
        input_ = '''Q S Q2 COS --images
1 A
2 B
3 C'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS "
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                                 <list_item id="3" name="" style="">
                                                                    <content>C</content>
                                                                 </list_item>
                                                 </control_single>
                                                 <control_layout id="Q2.js"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>
&lt;!-- Obrazki zamiast kafeterii --&gt;
&lt;script type='text/javascript'&gt;
var multiImageControlId = 'Q2';
&lt;/script&gt;</content>
                                                 </control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_list_column_3(self):
        input_ = '''Q S Q2 COS --listcolumn-3
1 A
2 B
3 C'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS "
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                                 <list_item id="3" name="" style="">
                                                                    <content>C</content>
                                                                 </list_item>
                                                 </control_single>
                                                 <control_layout id="Q2.js"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>
&lt;!-- list column --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
new IbisListColumn("Q2",3);
&lt;/script&gt;
</content>
                                                 </control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_list_column_default(self):
        input_ = '''Q S Q2 COS --listcolumn
1 A
2 B
3 C'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS "
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                                 <list_item id="3" name="" style="">
                                                                    <content>C</content>
                                                                 </list_item>
                                                 </control_single>
                                                 <control_layout id="Q2.js"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>
&lt;!-- list column --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
new IbisListColumn("Q2",2);
&lt;/script&gt;
</content>
                                                 </control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_list_column_10_col(self):
        input_ = '''Q S Q2 COS --listcolumn-10
1 A
2 B
3 C'''
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS "
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                 </list_item>
                                                                 <list_item id="3" name="" style="">
                                                                    <content>C</content>
                                                                 </list_item>
                                                 </control_single>
                                                 <control_layout id="Q2.js"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>
&lt;!-- list column --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
new IbisListColumn("Q2",10);
&lt;/script&gt;
</content>
                                                 </control_layout>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)


class TestParseToXmlControlMulti(KreaturaTestCase):
    def test_control_multi_xml(self):
        line = """Q M Q1 COS
A"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_multi id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_multi>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_control_multi_no_cafeteria(self):
        input_ = "Q M Q1 COS"
        survey = parse(input_)

        self.assertRaises(ValueError, survey.to_xml)


class TestParseToXmlControlNumber(KreaturaTestCase):
    def test_control_open_xml(self):
        line = "Q N Q1 COS"
        survey = parse(line)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_number id="Q1"
                                                               float="false"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1 | COS">
                                                               <content></content>
                                                 </control_number>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_controls_open_xml(self):
        line = """Q N Q1 COS
A
B"""
        survey = parse(line)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_number id="Q1_1"
                                                               float="false"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_1 | A">
                                                               <content></content>
                                                 </control_number>
                                                 <control_number id="Q1_2"
                                                               float="false"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_2 | B">
                                                               <content></content>
                                                 </control_number>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_controls_open_xml_explicite_id(self):
        line = """Q N Q1 COS
7 A
8 B"""
        survey = parse(line)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_number id="Q1_7"
                                                               float="false"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_7 | A">
                                                               <content></content>
                                                 </control_number>
                                                 <control_number id="Q1_8"
                                                               float="false"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1_8 | B">
                                                               <content></content>
                                                 </control_number>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)


class TestJsTables(KreaturaTestCase):
    def setUp(self):
        self.line = '''Q T Q1 COS
1 CAF A
_
1 STW A'''

        self.survey = parse(self.line)
        self.creationtime = self.survey.createtime

    def test_table(self):
        #                root  block     page
        question = self.survey.childs[0].childs[0].childs[0]

        caf = [Cafeteria(**{'id': '1', 'content': 'CAF A'})]
        stw = [Cafeteria(**{'id': '1', 'content': 'STW A'})]

        self.assertEqual(question.cafeteria, caf)
        self.assertEqual(question.statements, stw)

    def test_table_xml(self):

        self.survey.to_xml()
        got = etree.tostring(self.survey.xml, pretty_print=True)
        want = '''
<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
        name="CHANGEIT" sensitive="false" showbar="false" time="60000">
<block id="Default" name="" quoted="false" random="false" rotation="false">
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_1_txt" layout="default" style="">
<content>STW A</content>
</control_layout>
<control_single id="Q1_1" itemlimit="0" layout="vertical" name="Q1_1 | STW A" random="false" require="true"
                results="true" rotation="false" style="">
<list_item id="1" name="" style="">
<content>CAF A</content>
</list_item>
</control_single>
<control_layout id="Q1.js" layout="default" style="">
<content>
&lt;!-- tabela js --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/tables.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/tables.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table(&quot;Q1_&quot;);

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
&lt;/script&gt;

&lt;!-- custom css --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;
</content>

</control_layout>
</question>
</page>
</block>
<vars></vars>
<procedures>
<procedure id="PROC" shortdesc=""></procedure>
</procedures>
</survey>
'''.format(self.creationtime)

        self.assertXmlEqual(got, want)

    def test_table_no_statements(self):
        line = '''Q T Q1 COS
1 CAF A
2 STW A'''

        survey = parse(line)
        self.assertRaises(ValueError, survey.to_xml)

    def test_table_with_multi(self):
        input_ = """Q T Q1 COS --multi
1 A
2 B
_
2 B"""
        survey = parse(input_)
        survey.to_xml()
        got = etree.tostring(survey.xml)

        want = """<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
                          localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
<block id="Default" name="" quoted="false" random="false" rotation="false">
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_2_txt" layout="default" style="">
<content>B</content>
</control_layout>
<control_multi id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true" results="true"
               rotation="false" style="">
<list_item id="1" name="" style="">
<content>A</content>
</list_item>
<list_item id="2" name="" style="">
<content>B</content>
</list_item>
</control_multi>
<control_layout id="Q1.js" layout="default" style="">
<content>
&lt;!-- tabela js --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/tables.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/tables.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table(&quot;Q1_&quot;);

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
&lt;/script&gt;

&lt;!-- custom css --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;
</content>

</control_layout>
</question>
</page>
</block>
<vars></vars>
<procedures>
<procedure id="PROC" shortdesc=""></procedure>
</procedures>
</survey>""".format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_table_caf_with_hide(self):
        input_ = """Q T Q1 COS --multi
1 A --hide:$Q1:{0} == "1"
2 B
_
2 B"""
        survey = parse(input_)
        survey.to_xml()
        got = etree.tostring(survey.xml)

        want = """<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
                          localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
<block id="Default" name="" quoted="false" random="false" rotation="false">
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_2_txt" layout="default" style="">
<content>B</content>
</control_layout>
<control_multi id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true"
               results="true" rotation="false" style="">
<list_item id="1" name="" style="">
<content>A</content>
<hide><![CDATA[$Q1:1 == "1"]]></hide>
</list_item>
<list_item id="2" name="" style="">
<content>B</content>
<hide><![CDATA[$Q1:2 == "1"]]></hide>
</list_item>
</control_multi>
<control_layout id="Q1.js" layout="default" style="">
<content>
&lt;!-- tabela js --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/tables.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/tables.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table(&quot;Q1_&quot;);

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
&lt;/script&gt;

&lt;!-- custom css --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;
</content>

</control_layout>
</question>
</page>
</block>
<vars></vars>
<procedures>
<procedure id="PROC" shortdesc=""></procedure>
</procedures>
</survey>""".format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_statement_with_hide(self):
        input_ = '''Q T Q1 COS --multi
1 A
_
2 B --hide:$Q1:{0} == "1"'''

        survey = parse(input_)
        survey.to_xml()
        got = etree.tostring(survey.xml)

        want = """<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
                          localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
<block id="Default" name="" quoted="false" random="false" rotation="false">
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_2_txt" layout="default" style="">
<hide><![CDATA[$Q1:2 == "1"]]></hide>
<content>B</content>
</control_layout>
<control_multi id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$Q1:2 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>A</content>
</list_item>
</control_multi>
<control_layout id="Q1.js" layout="default" style="">
<content>
&lt;!-- tabela js --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/tables.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/tables.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table(&quot;Q1_&quot;);

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
&lt;/script&gt;

&lt;!-- custom css --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;</content>

</control_layout>
</question>
</page>
</block>
<vars></vars>
<procedures>
<procedure id="PROC" shortdesc=""></procedure>
</procedures>
</survey>""".format(survey.createtime)
        self.assertXmlEqual(got, want)


class TestErrors(KreaturaTestCase):
    def test_two_same_caf_numbers(self):
        input_ = """Q S Q1 COS
1 CAF A
1 CAF B"""
        survey = parse(input_)

        self.assertRaises(ValueError, survey.to_xml)


class TestWarnings(KreaturaTestCase):
    def test_many_columns_warning(self):
        text_input = """Q S Q1 COS --listcolumn-5
1 a"""

        survey = parse(text_input)
        survey.to_xml()

        expected = "W pytaniu Q1 wskazana liczba kolumn ma być większa niż 3. Nie za szeroko?"
        self.assertEqual(expected, survey.warnings[0])

if __name__ == "__main__":
    main()
