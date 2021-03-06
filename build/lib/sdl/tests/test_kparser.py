from lxml import etree
from sdl.kparser import parse, recognize
from sdl.elements import Block, Page, Question, Cafeteria, Survey
from sdl.tools import KreaturaTestCase, print_tree


# recognize
class TestRecognize(KreaturaTestCase):
    class TestBlock():
        def test_simple_block(self):
            line = "B B0"
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        def test_block_with_parrent(self):
            line = "B B0 B1"
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        def test_block_with_randomize(self):
            line = "B B0 --ran"
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        def test_block_with_rotation(self):
            line = "B B0 --rot"
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        def test_block_with_hide(self):
            line = 'B B0 --hide: $A0:{0} == "1"'
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        def test_block_all_possible(self):
            line = 'B B0 B1 --rot --hide: $A0:{0} == "1"'
            result = recognize(line)
            self.assertEqual("BLOCK", result)

        # tu będzie jednak cafeteria?
        # def test_block_error(self):
        #     line = 'B B0 B1 -rot'
        #     result = recognize(line)
        #     self.assertEqual(None, result)

        # def test_ran_rot_error(self):
        #     line = 'B B0 B1 --rot --ran'
        #     result = recognize(line)
        #     self.assertEqual(None, result)

        def test_block_to_many_parents(self):
            line = 'B B0 B1 B2 B3'
            result = recognize(line)
            self.assertEqual("CAFETERIA", result)

    class TestPage():

        def test_simple_page(self):
            line = "P P0"
            result = recognize(line)
            self.assertEqual("PAGE", result)

        def test_page_with_hide(self):
            line = 'P P0 --hide:$A1:{0} == "1"'
            result = recognize(line)
            self.assertEqual("PAGE", result)

        # Cafeteria
        # def test_page_with_rot(self):
        #     """Może z czasem ta rotacja bedzie potrzebna"""
        #     line = 'P P0 --rot --hide:$A1:{0} == "1"'
        #     result = recognize(line)
        #     self.assertEqual(None, result)

        def test_page_with_parent(self):
            line = 'P P0 --parent:MAIN'
            result = recognize(line)
            self.assertEqual('PAGE', result)



    class TestQuestionRecoginize():

        def test_simple_single(self):
            line = "Q S Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_multi(self):
            line = "Q M Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_layout(self):
            line = "Q L Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_numeric(self):
            line = "Q N Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_open(self):
            line = "Q O Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_open_with_size(self):
            line = "Q O90_4 Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_baskets_old(self):
            line = "Q LHS Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_baskets_new(self):
            line = "Q B Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_grid_old(self):
            line = "Q SDG Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_grid_new(self):
            line = "Q G Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_table_new(self):
            line = "Q T Q1 Treść"
            self.assertEqual("QUESTION", recognize(line))

        def test_simple_table_with_rot(self):
            line = "Q T Q1 Treść --rot"
            self.assertEqual("QUESTION", recognize(line))

        def test_question_with_parrent(self):
            line = "Q T Q1 Q0 Treść --rot"
            self.assertEqual("QUESTION", recognize(line))

        def test_question_with_hide(self):
            line = 'Q T Q1 Q0 Treść --hide: $A1:{0} == "1"'
            self.assertEqual("QUESTION", recognize(line))

        def test_q_with_deactivate(self):
            line = "Q O Q1 TRESC --d:'Nie wiem'"
            self.assertEqual('QUESTION', recognize(line))

        def test_slider(self):
            line = "Q SLIDER Q1 TRESC"
            self.assertEqual('QUESTION', recognize(line))

        def test_highlighter(self):
            line = "Q H Q1 COS"
            self.assertEqual('QUESTION', recognize(line))

        def test_concept_select(self):
            line = "Q CS Q1 COS"
            self.assertEqual('QUESTION', recognize(line))


    class TestSwitch():
        def test_switch(self):
            line = "_"
            self.assertEqual("SWITCH", recognize(line))

        def test_switch_with_spaces(self):
            line = "_  "
            self.assertEqual("SWITCH", recognize(line))

        def test_switch_double__(self):
            line = "__  "
            self.assertEqual("SWITCH", recognize(line))


    class TestPrecode():
        def test_simple_precode(self):
            line = 'PRE $Q1="1";$Q2="2"'
            self.assertEqual("PRECODE", recognize(line))

        def test_dim_style_commented_precode(self):
            line = "PRE ' if cos then cos"
            self.assertEqual("PRECODE", recognize(line))



    class TestPostcode():
        def test_simple_precode(self):
            line = 'POST $Q1="1";$Q2="2"'
            self.assertEqual("POSTCODE", recognize(line))

        def test_dim_style_commented_postcode(self):
            line = "POST ' if cos then cos"
            self.assertEqual("POSTCODE", recognize(line))


    class TestCafeteria():
        """kafeterie stwierdzen i odpowiedzi"""

        def test_just_number(self):
            line = "1"
            self.assertEqual("CAFETERIA", recognize(line))

        def test_just_word(self):
            line = "coś"
            self.assertEqual("CAFETERIA", recognize(line))

        def test_num_word_slash(self):
            line = "97 nie wiem/trudno powiedzieć"
            self.assertEqual("CAFETERIA", recognize(line))

        def test_num_word_backslash(self):
            line = r"97 nie wiem\trudno powiedzieć"
            self.assertEqual("CAFETERIA", recognize(line))

        def test_num_dot_word_backslash(self):
            line = r"97.d nie wiem\trudno powiedzieć"
            self.assertEqual("CAFETERIA", recognize(line))

        def test_num_dot_c(self):
            line = '97.c inne'
            self.assertEqual("CAFETERIA", recognize(line))

        def test_hide(self):
            line = '1 cos --hide:$A1:1 == "1"'
            self.assertEqual("CAFETERIA", recognize(line))

        def test_goto_and_hide(self):
            line = '98.d żadne z powyższych --hide:"0"--goto:B1_p'
            self.assertEqual('CAFETERIA', recognize(line))

        # to jednak cafeteria?
        # def test_wrong_call_two_hides(self):
        #     line = r'97.c nie wiem\trudno powiedzieć --hide:$A1:1 == "1" --hide:$A1:1 == "1"'
        #     self.assertEqual(None, recognize(line))

        def test_caf_screenout_nfo(self):
            line = '1 cos --so'
            self.assertEqual('CAFETERIA', recognize(line))

        def test_sign_in_cafeteria(self):
            line = 'a!@#$%^&*()_+-=.,'":;\|/[]{}`"
            line = '1 cos (PLN;EUR)'
            self.assertEqual('CAFETERIA', recognize(line))

        def test_real_test_1(self):
            line = '2 W wieku 5-9 lat'
            line2 = '3 W wieku 10-14 lat'
            line3 = '1.	Tak, kupuję je dość często'
            line4 = '2.001 - 3.000 zł'
            line5 = '2 Nie --goto:S7_p'
            line6 = "01 Ballantine's"
            line7 = 'A--hide:$P4B:{0} == "1"'
            line8 = "<p><strong>Aloe Balsam 100 %</strong> to najwyższej jakości, delikatny jak chusteczki papier" \
                    " toaletowy (3- warstwowy) z dodatkiem balsamu z aloesu i witaminy E.<br/> Przebadany " \
                    "dermatologicznie," \
                    " o PH przyjaznym dla sk&oacute;ry.</p><p>Doskonale zadba nawet o najbardziej wrażliwą" \
                    " sk&oacute;rę.</p>"

            self.assertEqual('CAFETERIA', recognize(line))
            self.assertEqual('CAFETERIA', recognize(line2))
            self.assertEqual('CAFETERIA', recognize(line3))
            self.assertEqual('CAFETERIA', recognize(line4))
            self.assertEqual('CAFETERIA', recognize(line5))
            self.assertEqual('CAFETERIA', recognize(line6))
            self.assertEqual('CAFETERIA', recognize(line7))
            self.assertEqual('CAFETERIA', recognize(line8))


    class TestBlank():
        def test_blank_line(self):
            line = ""
            self.assertEqual("BLANK", recognize(line))


    class TestComment():

        def test_comment_line(self):
            input_ = "// this is a comment"
            self.assertEqual("COMMENT", recognize(input_))

    class TestLoop():
        def test_loop_recognize(self):
            line = "FOR CATEGORIES:"
            result = recognize(line)

            self.assertEqual('LOOP', result)


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
        self.assertEqual(block.postcode, result.childs[0].postcode)

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

    def test_page_parent(self):
        text_input = """B MAIN
B B1
P P0 --parent:MAIN"""

        survey = Survey()
        block = Block('MAIN')
        b1 = Block('B1')
        page = Page('P0')
        page.parent_id = 'MAIN'
        block.childs.append(page)

        survey.append(block)
        survey.append(b1)

        got = parse(text_input)
        survey.createtime = got.createtime

        self.assertEqual(got, survey)
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
        q.dontknow = 'Nie wiem / trudno powiedzieć'
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
1 a --so
2 b --so"""

#         caf = Cafeteria()
#         caf.id = '1'
#         caf.content = 'a'
#         caf.screenout = True
#
#         q = Question('Q1')
#         q.typ = "S"
#         q.content = 'A'
#         q.cafeteria.append(caf)
#
#         p = Page('Q1_p')
#         p.childs.append(q)
#         p.postcode = """if ($Q1:1 == "1")
#   #OUT = "1"
#   goto KONKURS
# else
# endif"""
#         b = Block('Default')
#         b.childs.append(p)
#         survey = Survey()
#         survey.append(b)
#         survey.to_xml()

        result = parse(input_)
        result.to_xml()

        got = etree.tostring(result.xml)
        want = """  <survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
        localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>A</content>
          </control_layout>
          <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 | A" random="false" require="true"
          results="true" rotation="false" style="">
            <list_item id="1" name="" style="">
              <content>a</content>
            </list_item>
            <list_item id="2" name="" style="">
              <content>b</content>
            </list_item>
          </control_single>
        </question>
        <postcode>if ($Q1:1 == &quot;1&quot;)
  #OUT = &quot;1&quot;
  goto KONKURS
else
endif

if ($Q1:2 == &quot;1&quot;)
  #OUT = &quot;1&quot;
  goto KONKURS
else
endif</postcode>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>""".format(result.createtime)
        self.assertXmlEqual(got, want)

    def test_nesting(self):
        input_ = """B MAIN
B B1 MAIN
Q L Q1 cos

B B2 MAIN
Q L Q2 cos

P P3_p --parent:MAIN
Q L Q3 cos
"""
        survey = parse(input_)

        want = Survey()
        want.createtime = survey.createtime

        b_main = Block('MAIN')

        b_b1 = Block('B1')
        p = Page('Q1_p')
        q = Question('Q1')
        q.typ = 'L'
        q.content = 'cos'
        p.childs.append(q)
        b_b1.childs.append(p)

        b_b2 = Block('B2')
        b_b2.parent_id = "MAIN"
        p = Page('Q2_p')
        q = Question('Q2')
        q.typ = 'L'
        q.content = 'cos'
        p.childs.append(q)
        b_b2.childs.append(p)

        p = Page('P3_p')
        p.parent_id = "MAIN"
        q = Question('Q3')
        q.typ = 'L'
        q.content = 'cos'
        p.childs.append(q)

        b_main.childs.append(b_b1)
        b_main.childs.append(b_b2)
        b_main.childs.append(p)

        want.append(b_main)

        # print(print_tree(survey))
        # print(print_tree(want))

        got = print_tree(survey)
        want = print_tree(want)
        self.assertEqual(got, want)

    def test_question_hide_xml(self):
        # TODO: hide dla question?
        input_ = '''Q O Q1 A --hide:#POKAZ_1 == "0"'''
        survey = parse(input_)
        survey.to_xml()
        got = etree.tostring(survey.xml)

        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>A</content>
        </control_layout>
        <control_open id="Q1_OPEN" length="25" lines="1" mask=".*" name="Q1 | A " require="true" results="true" style="">
          <content/>
        </control_open>
        <hide><![CDATA[#POKAZ_1 == "0"]]></hide>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)

    # endregion


class TextParseToXml(KreaturaTestCase):
    def test_goto(self):
        line = """Q S Q1 COS
A --goto: A4_p

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
    goto A4_p
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

    def test_2_cond_in_hide(self):
        input_ = '''Q S Q2 COS
1 A --hide:$Q1:{0} == "1" || $Q1a:{0} == "1"
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
                                                                    <hide><![CDATA[$Q1:1 == "1" || $Q1a:1 == "1"]]></hide>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                    <hide><![CDATA[$Q1:2 == "1" || $Q1a:2 == "1"]]></hide>
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

    def test_sliders(self):
        input_ = """Q SLIDERS Q1 COS
left: left_end
right: right_end
_
01 A
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        # print(etree.tostring(survey.xml, pretty_print=True))

        got = etree.tostring(survey.xml)
        want = '''  <survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
     sliderOpts = {{
          value: 0,
          min: 1,
          max: 10,
          step: 1,
          animate:&quot;slow&quot;,
          orientation: 'horizontal'
     }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

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
  </survey>
'''.format(ct)
        self.assertXmlEqual(got, want)

    def test_sliders_with_ran(self):
        input_ = """Q SLIDERS Q1 COS --ran
left: left_end
right: right_end
_
01 A
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        # print(etree.tostring(survey.xml, pretty_print=True))

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
     sliderOpts = {{
          value: 0,
          min: 1,
          max: 10,
          step: 1,
          animate:&quot;slow&quot;,
          orientation: 'horizontal'
     }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

&lt;/script&gt;

&lt;script type='text/javascript' src='public/rotate_tables.js'&gt;&lt;/script&gt;
&lt;!-- get the file from https://github.com/rkorzen/ibisjs
     optionally uncomment the line bellow (only for tests - never for production!!)
--&gt;
&lt;!--
&lt;script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'&gt;&lt;/script&gt;
&lt;link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'&gt;
--&gt;</content>
          </control_layout>
        </question>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>
'''.format(ct)
        self.assertXmlEqual(got, want)

    def dtest_sliders_with_hide(self):
        input_ = """Q SLIDERS Q1 COS --ran
left: left_end
right: right_end
_
01 A--hide:$Q1:{0} == "1"
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:01 == "1"]]></hide>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:02 == "1"]]></hide>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:03 == "1"]]></hide>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
 sliderOpts = {{
      value: 0,
      min: 1,
      max: 10,
      step: 1,
      animate:&quot;slow&quot;,
      orientation: 'horizontal'
 }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

&lt;/script&gt;

&lt;script type='text/javascript' src='public/rotate_tables.js'&gt;&lt;/script&gt;
&lt;!-- get the file from https://github.com/rkorzen/ibisjs
     optionally uncomment the line bellow (only for tests - never for production!!)
--&gt;
&lt;!--
&lt;script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'&gt;&lt;/script&gt;
&lt;link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'&gt;
--&gt;

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
'''.format(ct)

        self.assertXmlEqual(got, want)

    def test_colon_in_cafeteria(self):
        input_ = """Q M Q1 COS
1 A: B
"""
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
                                                                    <content>A: B</content>
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

    def test_hide_and_space(self):
        input_ = '''Q M Q1 COS
A--hide:$P4B:{0} == "1"'''

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
                                                                    <hide><![CDATA[$P4B:1 == "1"]]></hide>
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


# Block
class TestParseToXmlBlock(KreaturaTestCase):
    def test_block_with_precode(self):
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

    def test_block_postcode(self):
        input_ = 'B B0\nPOST $A1="1"'

        result = parse(input_)
        result.to_xml()
        r_xml = etree.tostring(result.xml)

        expected = Survey()
        expected.createtime = result.createtime
        expected.append(Block('B0'))
        expected.childs[0].postcode = '$A1="1"'
        expected.to_xml()

        e_xml = etree.tostring(expected.xml)

        self.assertEqual(expected, result)
        self.assertXmlEqual(r_xml, e_xml)

    def test_block_precode_postcode(self):
        input_ = '''B B0
PRE $A1="1"
POST $A1="2"'''

        result = parse(input_)
        result.to_xml()
        r_xml = etree.tostring(result.xml)

        expected = Survey()
        expected.createtime = result.createtime
        expected.append(Block('B0'))
        expected.childs[0].precode = '$A1="1"'
        expected.childs[0].postcode = '$A1="2"'
        expected.to_xml()
        e_xml = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
        name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="B0" name="" quoted="false" random="false" rotation="false">
    <precode><![CDATA[$A1="1"]]></precode>
    <postcode><![CDATA[$A1="2"]]></postcode>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
""".format(result.createtime)

        self.assertEqual(expected, result)
        self.assertXmlEqual(r_xml, e_xml)


# Page
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
        want = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
        name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="P0" hideBackButton="false" name="">
      <precode><![CDATA[if($A1:1 == "1")
  goto next
else
endif]]></precode>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
""".format(result.createtime)

        self.assertEqual(expected, result)
        self.assertXmlEqual(got, want)

    def test_page_precode_value_error(self):
        input_ = 'P P0\nPRE if($A1:1 == "1");goto next;endif'
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_xml)


# Open
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
                                                 <control_open id="Q1_OPEN"
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

    def test_control_open_not_require(self):
        line = "Q O Q1 COS--nr"
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
                                                 <control_open id="Q1_OPEN"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="false"
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

    def test_controls_open_not_require(self):
        line = "Q O Q1 COS--nr\n1\n2" \

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
                                                               require="false"
                                                               results="true"
                                                               style=""
                                                               name="Q1_1 | 1">
                                                               <content></content>
                                                 </control_open>
                                                 <control_open id="Q1_2"
                                                               length="25"
                                                               lines="1"
                                                               mask=".*"
                                                               require="false"
                                                               results="true"
                                                               style=""
                                                               name="Q1_2 | 2">
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
                                                 <control_open id="Q1_OPEN"
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
        line = "Q O90_4 Q1 COS --dk:"
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
                                                 <control_open id="Q1_OPEN"
                                                               length="90"
                                                               lines="4"
                                                               mask=".*"
                                                               require="true"
                                                               results="true"
                                                               style=""
                                                               name="Q1 | COS">
                                                               <content></content>
                                                 </control_open>
<control_layout id="Q1_OPEN.js" layout="default" style="">
<content>
&lt;!-- dezaktywacja opena --&gt;
&lt;script type='text/javascript'&gt;
    var opendisDest = "Q1_OPEN";
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


# Text
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

    def test_cl_with_css(self):
        line = """Q L Q1 COS --custom_css"""
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
                                                 <control_layout id="Q1_css"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>&lt;link rel="stylesheet"
                                                                 href="public/custom.css" type="text/css"&gt;</content>
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


# Single
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
<postcode><![CDATA[if ($Q1:2 == "1")
  #OUT = "1"
  goto KONKURS
else
endif

]]>
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
        input_ = '''Q S Q2 COS --listcolumn:3
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
        input_ = '''Q S Q2 COS --listcolumn:10
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

    def test_goto(self):
        line = """Q S Q1 COS
A--goto:A2_p

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
    goto A2_p
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

    def test_randomize(self):
        line = """Q S Q1 COS --ran
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
                                                                 random="true"
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

    def test_rotation(self):
        line = """Q S Q1 COS --rot
A"""
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        # print(got)
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
                                                                 rotation="true"
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

    def test_connected_with_open(self):
        input_ = '''Q S Q1 COS
1.c A'''
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
                                                                 <list_item id="1" name="" style="" connected="Q1_1T">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                                 <control_open id="Q1_1T" length="25" lines="1" mask=".*"
                                                 name="Q1_1T | A" require="true" results="true" style="">
                                                    <content/>
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

    def test_single_to_dim(self):
        input_ = """Q S Q4 W jakiej wielkości miejscowości mieszkasz?
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
    Categorical [1..1]
    {
        _1 "wieś",
        _2 "miasto do 20 tys. mieszkańców",
        _3 "miasto 20.000-49.999 mieszkańców",
        _4 "miasto 50.000-99.999 mieszkańców",
        _5 "miasto 100.000-199.999 mieszkańców",
        _6 "miasto 200.000-499.999 mieszkańców",
        _7 "miasto 500.000 mieszkańców lub większe",
        _8 "nie wiem/ trudno powiedzieć"

    };
'''

        self.assertTxtEqual(got, want)

    def test_postcode(self):
        text = '''Q S Q1 COS
POST #TEST = "1"
A
B'''
        survey = parse(text)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
        name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>COS</content>
        </control_layout>
        <control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS" random="false" require="true"
        results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>A</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>B</content>
          </list_item>
        </control_single>
      </question>
      <postcode><![CDATA[#TEST = "1"]]></postcode>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>""".format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_postcode_with_if(self):
        text = '''Q S Q1 COS
POST if($Q1:1 == "1");else;goto next;endif
A
B'''
        survey = parse(text)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
        localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>COS</content>
        </control_layout>
        <control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS" random="false"
         require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>A</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>B</content>
          </list_item>
        </control_single>
      </question>
      <postcode><![CDATA[if($Q1:1 == "1")
else
  goto next
endif
]]></postcode>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>""".format(survey.createtime)

        self.assertXmlEqual(got, want)

    def test_postcode_with_2_ifs(self):
        text = """Q S S6 Na kogo głosował(a) Pan(i) w drugiej turze wyborów prezydenckich?
POST if(#ROK >= "1985" && $S6:2=="1");gr2="10";else;endif;;if(#ROK < "1985" && $S6:2=="1");gr2="01";else;endif
1 a --so"""
        survey = parse(text)
        survey.to_xml()

        expected = """<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="S6_p" hideBackButton="false" name="">
      <question id="S6" name="">
        <control_layout id="S6.labelka" layout="default" style="">
          <content>Na kogo g&#322;osowa&#322;#END_A# #SEX_M# w drugiej turze wybor&#243;w prezydenckich?</content>
        </control_layout>
        <control_single id="S6" layout="vertical" style="" itemlimit="0" name="S6 | Na kogo g&#322;osowa&#322;(a) Pan(i) w drugiej turze wybor&#243;w prezydenckich?" random="false" require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_single>
      </question>
      <postcode><![CDATA[if(#ROK >= "1985" && $S6:2=="1")
  gr2="10"
else
endif

if(#ROK < "1985" && $S6:2=="1")
  gr2="01"
else
endif

if ($S6:1 == "1")
  #OUT = "1"
  goto KONKURS
else
endif

]]></postcode>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>""".format(survey.createtime)


        result = etree.tostring(survey.xml, pretty_print=True)
        self.assertXmlEqual(result, expected)

# Multi
class TestParseToXmlControlMulti(KreaturaTestCase):
    def setUp(self):
        self.maxDiff = None

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

    def test_control_multi_min_precode(self):
        input_ = '''Q M Q1 COS--minchoose:2
PRE $A="0"
A'''
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
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <precode>$A=&quot;0&quot;</precode>
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
                                                                 minchoose="2"
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

    def test_multi_min(self):
        input_ = '''Q M Q1 COS--minchoose:2
A'''
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
                                                                 minchoose="2"
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

    def test_multi_min_max(self):
        input_ = '''Q M Q1 COS--minchoose:2--maxchoose:2
A'''
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
                                                                 minchoose="2"
                                                                 maxchoose="2"
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

    def test_disablerest(self):
        input_ = """Q M Q1 COS
A
98.d B"""

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
                                                         <list_item id="98" name="" style="" disablerest="true">
                                                            <content>B</content>
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


# Number
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


# js table
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

    def test_statements_with_hide(self):
        input_ = '''Q T Q1 COS
a
b
_
A--hide:$Q1:{0} == "1"
B'''
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
<control_layout id="Q1_1_txt" layout="default" style="">
<hide><![CDATA[$Q1:1 == "1"]]></hide>
<content>A</content>
</control_layout>
<control_single id="Q1_1" itemlimit="0" layout="vertical" name="Q1_1 | A" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$Q1:1 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
</list_item>
</control_single>
<control_layout id="Q1_2_txt" layout="default" style="">
<hide><![CDATA[$Q1:2 == "1"]]></hide>
<content>B</content>
</control_layout>
<control_single id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$Q1:2 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
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

    def test_statements_hide_diffrent(self):
        input_ = '''Q T Q1 COS
a
b
_
A--hide:$K1:{0} == "1"
B--hide:$K2:{0} == "1"'''
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
<control_layout id="Q1_1_txt" layout="default" style="">
<hide><![CDATA[$K1:1 == "1"]]></hide>
<content>A</content>
</control_layout>
<control_single id="Q1_1" itemlimit="0" layout="vertical" name="Q1_1 | A" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$K1:1 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
</list_item>
</control_single>
<control_layout id="Q1_2_txt" layout="default" style="">
<hide><![CDATA[$K2:2 == "1"]]></hide>
<content>B</content>
</control_layout>
<control_single id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$K2:2 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
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

    def test_statements_hide_and_no_hide(self):
        input_ = '''Q T Q1 COS
a
b
_
A--hide:$K1:{0} == "1"
B--hide:"0"'''
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
<control_layout id="Q1_1_txt" layout="default" style="">
<hide><![CDATA[$K1:1 == "1"]]></hide>
<content>A</content>
</control_layout>
<control_single id="Q1_1" itemlimit="0" layout="vertical" name="Q1_1 | A" random="false" require="true"
               results="true" rotation="false" style="">
<hide><![CDATA[$K1:1 == "1"]]></hide>
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
</list_item>
</control_single>
<control_layout id="Q1_2_txt" layout="default" style="">
<content>B</content>
</control_layout>
<control_single id="Q1_2" itemlimit="0" layout="vertical" name="Q1_2 | B" random="false" require="true"
               results="true" rotation="false" style="">
<list_item id="1" name="" style="">
<content>a</content>
</list_item>
<list_item id="2" name="" style="">
<content>b</content>
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


# slider
class TestSlider(KreaturaTestCase):
    def test_slider(self):
        line = "Q SLIDER Q1 TRESC"
        survey = parse(line)
        survey.to_xml()

        got = etree.tostring(survey.xml)

        want = """<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
        localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>TRESC</content>
          </control_layout>
          <control_number float="false" id="Q1" mask=".*" name="Q1 TRESC" require="true" results="true" style="">
            <content></content>
          </control_number>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;!-- Script name/version: slider/1.0 --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider3/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/slider3/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider3/slider_sog.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/slider3/slider_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
     sliderOpts = {{
          value: 1,
          min: 1,
          max: 10,
          step: 1,
          animate:&quot;slow&quot;,
          orientation: 'horizontal'
     }};

new IbisSlider(&quot;Q1&quot;, sliderOpts);
&lt;/script&gt;
&lt;!-- ControlScript ENDS HERE: slider --&gt;</content>
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

    def test_slider_with_ends(self):
        line = '''Q SLIDER Q1 TRESC
lewy koniec
prawy koniec'''

        survey = parse(line)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = """<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray"
        localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>TRESC</content>
          </control_layout>
          <control_table id="Q1_table" random='false' rotation='false' rrdest='row' style=''>
          <row forcestable='true' style=''>
          <cell colspan='1' forcestable='false' rowspan='1' style=''>
            <control_layout id='Q1left' layout="default" style="">
                <content>lewy koniec</content>
            </control_layout>
          </cell>
          <cell colspan='1' forcestable='false' rowspan='1' style=''>
              <control_number float="false" id="Q1" mask=".*" name="Q1 | lewy koniec - prawy koniec | TRESC "
              require="true" results="true" style="">
                <content></content>
              </control_number>
          </cell>
          <cell colspan='1' forcestable='false' rowspan='1' style=''>
            <control_layout id='Q1right' layout="default" style="">
                <content>prawy koniec</content>
            </control_layout>
          </cell>
          </row>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;!-- Script name/version: slider/1.0 --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider3/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/slider3/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider3/slider_sog.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/slider3/slider_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
     sliderOpts = {{
          value: 1,
          min: 1,
          max: 10,
          step: 1,
          animate:&quot;slow&quot;,
          orientation: 'horizontal'
     }};

new IbisSlider(&quot;Q1&quot;, sliderOpts);
&lt;/script&gt;
&lt;!-- ControlScript ENDS HERE: slider --&gt;</content>
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

    def test_slider_only_one_end(self):
        line = "Q SLIDER Q1 TRESC\nlewy koniec"
        survey = parse(line)
        self.assertRaises(ValueError, survey.to_xml)


# dinamic grid
class TestDinamicGrid(KreaturaTestCase):
    def test_dinamic_grid(self):
        line = '''Q G Q1 COS
1 a
_
1 stw a'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_single id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
         require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_single>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_dinamic_grid_multi(self):
        line = '''Q G Q1 COS
1 a
_
1 stw a--multi'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_multi id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
         require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_multi>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_dinamic_grid_multi_hide(self):
        line = '''Q G Q1 COS
1 a
_
1 stw a--multi --hide:A'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
      <hide><![CDATA[A]]></hide>
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_multi id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
         require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_multi>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_dinamic_grid_multi_hide_maxchoice(self):
        line = '''Q G Q1 COS--maxchoose:5
1 a
_
1 stw a--multi --hide:A'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
      <hide><![CDATA[A]]></hide>
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_multi id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
        require="true" results="true" rotation="false" maxchoose="5">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_multi>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_dinamic_grid_single_and_open(self):
        line = '''Q G Q1 COS
1.c a
_
1 stw a'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
        name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_single id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
        require="true" results="true" rotation="false">
          <list_item id="1" name="" style="" connected="Q1_1_1T">
            <content>a</content>
          </list_item>
        </control_single>
        <control_open id="Q1_1_1T" length="25" lines="1" mask=".*" name="Q1_1_1T | a" require="true" results="true"
        style="">
         <content/>
        </control_open>

      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_dinamic_grid_to_dim_single(self):
        input_ = """Q G Q1 COS
a
b
_
stw 1
stw 2
"""
        survey = parse(input_)
        survey.to_dim()
        got = survey.dim_out
        # print(got)
        want = """
    Q1 "COS"
        [
            flametatype = "mbdynamicgrid"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        ]
    loop
    {
        _1 "stw 1",
        _2 "stw 2"

    } fields -
    (
        slice ""
        categorical [1..1]
        {
            _1 "a",
            _2 "b"

        };
    ) expand grid;
"""

        self.assertTxtEqual(got, want)

    def test_grid_with_rotation(self):
        """Fix isue#8"""
        line = '''Q G Q1 COS
1 a
_
1 stw a--multi--rot'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_multi id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="false"
         require="true" results="true" rotation="true">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_multi>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_grid_with_random(self):
        """Fix isue#8"""
        line = '''Q G Q1 COS
1 a
_
1 stw a--multi--ran'''
        survey = parse(line)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl"
         name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false">
      <question id="Q1instr">
        <control_layout id="Q1_lab_instr" layout="default" style="">
          <content>&lt;div class="grid_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
      </question>
      <question id="Q1_1">
        <control_layout id="Q1_1_txt" layout="default" style="">
          <content>stw a</content>
        </control_layout>
        <control_multi id="Q1_1" layout="vertical" style="" itemlimit="0" name="Q1_1 | stw a" random="true"
         require="true" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>a</content>
          </list_item>
        </control_multi>
      </question>
      <question id="Q1script_calls">
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script: listcolumn --&gt;
&lt;link rel="stylesheet" href="public/listcolumn/listcolumn.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/listcolumn/listcolumn.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla list kolumn
  // u&#380;yj, gdy listy maj&#261; by&#263; podzielone na kolumny - np gdy bardzo d&#322;uga lista
  // new IbisListColumn("Q1_1",2);
&lt;/script&gt;
&lt;!-- end: listcolumn --&gt;

&lt;!-- Script: SuperImages --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/superImages.css'/&gt;
&lt;script type='text/javascript' src='public/superImages.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
  // przyk&#322;ad dla SuperImages
  // u&#380;yj je&#347;li maj&#261; by&#263; w gridzie obrazki zamiast kafeterii tekstowej
  // s1 = new SuperImages("Q1_1", {{zoom: false}});
&lt;/script&gt;
&lt;!-- end: SuperImages --&gt;

&lt;!-- Script: MerryGoRound --&gt;
&lt;link rel='stylesheet' type='text/css' href='public/merryGoRound.css'/&gt;
&lt;script type='text/javascript' src='public/merryGoRound.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
    mgr = new MerryGoRound(jQuery("div.question").slice(1,-1),{{randomQuestion: false}});
&lt;/script&gt;
&lt;!-- end: MerryGoRound --&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
      </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)
        self.assertXmlEqual(got, want)


# highlighter
class TestHiglighter(KreaturaTestCase):
    def test_highlighter(self):
        input_ = "Q H Q1 COS\npublic/X4_2.jpg"
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
                                         <control_layout id="Q1.js"
                                                         layout="default"
                                                         style="">
                                                         <content>&lt;script type='text/javascript' src='public/highlighter/highlighter.js'&gt;&lt;/script&gt;
&lt;link rel='stylesheet' type='text/css' href='public/highlighter/highlighter.css'/&gt;
&lt;script type='text/javascript'&gt;
hl = new IbisHighlighter('Q1.img','Q1.input', {{ hlClass: 'hl-active-green', debug: false }})
&lt;/script&gt;</content>
                                         </control_layout>
                                         <control_layout id="Q1.img" layout="default" style="">
                                           <content>&lt;img src="public/X4_2.jpg"&gt;</content>
                                         </control_layout>

                                         <control_open id="Q1.input"
                                                       length="25"
                                                       lines="1"
                                                       mask=".*"
                                                       require="true"
                                                       results="true"
                                                       style=""
                                                       name="Q1.input">
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

    def test_highlighter_no_img(self):
        input_ = "Q H Q1 COS"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_xml)


# baskets
class TestBaskets(KreaturaTestCase):
    def test_ibis_baskets(self):
        input_ = """Q LHS Q1 COS
1 1
2 2
_
1 A
2 B"""
        survey = parse(input_)
        survey.to_xml()
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
  <page id="Q1_p" hideBackButton="false" name="">
    <question id="Q1" name="">
      <control_layout id="Q1.labelka" layout="default" style="">
        <content>&lt;div class="basket_instrukcja"&gt;COS&lt;/div&gt;</content>
      </control_layout>
      <control_single id="Q1" itemlimit="0" layout="vertical" name="COS" random="false" require="false" results="true"
       rotation="false" style="">
        <list_item id="1" name="" style="">
          <content>&lt;img src="public/Q1/1.jpg" alt = "1"&gt;</content>
        </list_item>
        <list_item id="2" name="" style="">
          <content>&lt;img src="public/Q1/2.jpg" alt = "2"&gt;</content>
        </list_item>
      </control_single>
      <control_multi id="Q1x1" itemlimit="0" layout="vertical" name="Q1x1 | A" random="false" require="false"
       results="true" rotation="false" style="">
        <list_item id="1" name="" style="">
          <content>&lt;img src="public/Q1/1.jpg" alt = "1"&gt;</content>
        </list_item>
        <list_item id="2" name="" style="">
          <content>&lt;img src="public/Q1/2.jpg" alt = "2"&gt;</content>
        </list_item>
      </control_multi>
      <control_multi id="Q1x2" itemlimit="0" layout="vertical" name="Q1x2 | B" random="false" require="false"
       results="true" rotation="false" style="">
        <list_item id="1" name="" style="">
          <content>&lt;img src="public/Q1/1.jpg" alt = "1"&gt;</content>
        </list_item>
        <list_item id="2" name="" style="">
          <content>&lt;img src="public/Q1/2.jpg" alt = "2"&gt;</content>
        </list_item>
      </control_multi>
      <control_layout id="Q1.js" layout="default" style="">
<content>&lt;!-- Baskets --&gt;
&lt;script type="text/javascript" src="public/baskets/jquery-ui/js/jquery-ui-1.8.18.custom.min.js"&gt;&lt;/script&gt;
&lt;link rel="stylesheet" href="public/baskets/jquery-ui/css/ui-lightness/jquery-ui-1.8.18.custom.css" type="text/css"&gt;
&lt;script type="text/javascript" src="public/baskets/baskets.js"&gt;&lt;/script&gt;
&lt;link rel="stylesheet" href="public/baskets/baskets.css" type="text/css"&gt;
&lt;script type="text/javascript"&gt;
var bm = new BasketManager({{className: "multi", dest: "Q1"}});
bm.createBasket("Q1", {{
    source: true,
    max: 0
}});
bm.createBasket("Q1x1", {{
    label: "A",
    min: 0,
    max: 2,
    maxreplace: true
}});
bm.createBasket("Q1x2", {{
    label: "B",
    min: 0,
    max: 2,
    maxreplace: true
}});

&lt;/script&gt;
&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
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

        got = etree.tostring(survey.xml)
        self.assertXmlEqual(got, want)

    def test_ibis_baskets_lhs(self):
            input_ = """Q LHS Q1 COS
1 A
2 B
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
5 Love it"""
            survey = parse(input_)
            survey.to_xml()
            want = '''<survey createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false">
  <block id="Default" name="" quoted="false" random="false" rotation="false">
    <page id="Q1_p" hideBackButton="false" name="">
      <question id="Q1" name="">
        <control_layout id="Q1.labelka" layout="default" style="">
          <content>&lt;div class="basket_instrukcja"&gt;COS&lt;/div&gt;</content>
        </control_layout>
        <control_single id="Q1" layout="vertical" style="" itemlimit="0" name="COS" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_single>
        <control_multi id="Q1x1" layout="vertical" style="" itemlimit="0" name="Q1x1 | -5 Hate it" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x2" layout="vertical" style="" itemlimit="0" name="Q1x2 | -4" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x3" layout="vertical" style="" itemlimit="0" name="Q1x3 | -3" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x4" layout="vertical" style="" itemlimit="0" name="Q1x4 | -2" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x5" layout="vertical" style="" itemlimit="0" name="Q1x5 | -1" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x6" layout="vertical" style="" itemlimit="0" name="Q1x6 | 0 Neutral" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x7" layout="vertical" style="" itemlimit="0" name="Q1x7 | 1" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x8" layout="vertical" style="" itemlimit="0" name="Q1x8 | 2" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x9" layout="vertical" style="" itemlimit="0" name="Q1x9 | 3" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x10" layout="vertical" style="" itemlimit="0" name="Q1x10 | 4" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_multi id="Q1x11" layout="vertical" style="" itemlimit="0" name="Q1x11 | 5 Love it" random="false" require="false" results="true" rotation="false">
          <list_item id="1" name="" style="">
            <content>&lt;img src="public/Q1/1.jpg" alt = "A"&gt;</content>
          </list_item>
          <list_item id="2" name="" style="">
            <content>&lt;img src="public/Q1/2.jpg" alt = "B"&gt;</content>
          </list_item>
        </control_multi>
        <control_layout id="Q1.js" layout="default" style="">
          <content>&lt;!-- Baskets --&gt;
&lt;script type="text/javascript" src="public/baskets/jquery-ui/js/jquery-ui-1.8.18.custom.min.js"&gt;&lt;/script&gt;
&lt;link rel="stylesheet" href="public/baskets/jquery-ui/css/ui-lightness/jquery-ui-1.8.18.custom.css" type="text/css"&gt;
&lt;script type="text/javascript" src="public/baskets/baskets.js"&gt;&lt;/script&gt;
&lt;link rel="stylesheet" href="public/baskets/baskets.css" type="text/css"&gt;
&lt;script type="text/javascript"&gt;
var bm = new BasketManager({{className: "multi", dest: "Q1"}});
bm.createBasket("Q1", {{
    source: true,
    max: 0
}});
bm.createBasket("Q1x1", {{
    label: "-5 Hate it",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x2", {{
    label: "-4",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x3", {{
    label: "-3",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x4", {{
    label: "-2",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x5", {{
    label: "-1",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x6", {{
    label: "0 Neutral",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x7", {{
    label: "1",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x8", {{
    label: "2",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x9", {{
    label: "3",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x10", {{
    label: "4",
    min: 0,
    max: 11,
    maxreplace: true
}});
bm.createBasket("Q1x11", {{
    label: "5 Love it",
    min: 0,
    max: 11,
    maxreplace: true
}});

&lt;/script&gt;
&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;</content>
        </control_layout>
      </question>
    </page>
  </block>
  <vars/>
  <procedures>
    <procedure id="PROC" shortdesc=""/>
  </procedures>
</survey>
'''.format(survey.createtime)

            got = etree.tostring(survey.xml)
            self.assertXmlEqual(got, want)

    def test_no_kafeteria(self):
        line = "Q B Q1 COS"
        survey = parse(line)

        self.assertRaises(ValueError, survey.to_xml)

    def test_no_statements(self):
        line = "Q B Q1 COS\n1 a"
        survey = parse(line)

        self.assertRaises(ValueError, survey.to_xml)

    def test_no_caf_but_statements(self):
        line = "Q B Q1 COS\n_\n1 a"
        survey = parse(line)

        self.assertRaises(ValueError, survey.to_xml)

    def test_rotation(self):
        line = """Q B Q1 COS --rot\n1 a\n_\n1 a"""
        survey = parse(line)
        survey.to_xml()
        single = survey.xml.findall('.//control_single')[0]
        self.assertEqual(single.attrib['rotation'], 'true')

    def test_random(self):
        line = """Q B Q1 COS --ran\n1 a\n_\n1 a"""
        survey = parse(line)
        survey.to_xml()
        single = survey.xml.findall('.//control_single')[0]
        self.assertEqual(single.attrib['random'], 'true')


# ranking
class TestRanking(KreaturaTestCase):
    def test_ranking(self):
        input_ = '''Q R Q1 COS
a
b
c'''
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
                          <block id="Default" quoted="false" random="false" rotation="false" name="">
                                 <page id="Q1_p">
                                    <question id="Q1instr">
                                      <control_layout id="Q1_lab_instr" layout="default" style="">
                                        <content>&lt;div class="ranking_instrukcja"&gt;COS&lt;/div&gt;</content>
                                      </control_layout>
                                    </question>
                                    <question id="Q1">
      <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 | COS" random="false" require="false"
       results="true" rotation="false" style="">
        <list_item id="1" name="" style="">
          <content>a</content>
        </list_item>
        <list_item id="2" name="" style="">
          <content>b</content>
        </list_item>
        <list_item id="3" name="" style="">
          <content>c</content>
        </list_item>
      </control_single>
      <control_number id="Q1.number1" float="false" mask=".*" require="true" results="true" style=""
       name="Pozycja Odp1"><content></content></control_number>
      <control_number id="Q1.number2" float="false" mask=".*" require="true" results="true" style=""
       name="Pozycja Odp2"><content></content></control_number>
      <control_number id="Q1.number3" float="false" mask=".*" require="true" results="true" style=""
       name="Pozycja Odp3"><content></content></control_number>
      <control_layout id="Q1.js" layout="default" style="">
        <content>&lt;!-- Script Ranking --&gt;
&lt;link rel=stylesheet type=text/css href="public/ranking.css"&gt;
&lt;script type='text/javascript' src='public/jquery-ui-1.7.2.custom.min.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript' src='public/ranking.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;addRanking("Q1");&lt;/script&gt;
&lt;!-- end Script Ranking --&gt;

&lt;link rel=stylesheet type=text/css href="public/custom.css"&gt;
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


# concept select
class TestConceptSelect(KreaturaTestCase):

    def test_no_concept_select_text(self):
        input_ = "Q CS Q1 COS"
        survey = parse(input_)
        self.assertRaises(ValueError, survey.to_xml)

    def test_concept_select(self):
        input_ = """Q CS Q1 COS
A B"""
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
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_tresc" layout="default" style="">
<content>A | B</content>
</control_layout>
<control_open id="Q1_data" length="25" lines="1" mask=".*" name="Q1_data | ConceptSelect" require="true"
 results="true" style="display:none;">
<content/>
</control_open>
<control_multi id="Q1_dis" itemlimit="0" layout="vertical" name="Q1_dis" random="false" require="false"
 results="true" rotation="false" style="">
<list_item id="98" name="" style="">
<content>Nic nie zwróciło mojej uwagi</content>
</list_item>
</control_multi>
<control_layout id="Q1.js" layout="default" style="">
<content>&lt;script type='text/javascript' src='public/ibisDisabler.js'&gt;&lt;/script&gt;
&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.98','Q1_tresc');
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.98','Q1_data',98);
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Concept Select  --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/Selection_sog.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/Selection_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
var sel = new Selection({{
textContainerId: &quot;Q1_tresc&quot;,
openContainerId: &quot;Q1_data&quot;,
delimiter: &quot;|&quot;
}});
&lt;/script&gt;
&lt;!-- End ConceptSelect --&gt;</content>
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

    def test_concept_select_custom_disabler(self):
        input_ = """Q CS Q1 COS
A B
_
97 Odmowa
98 Nie wiem"""
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
<page hideBackButton="false" id="Q1_p" name="">
<question id="Q1" name="">
<control_layout id="Q1.labelka" layout="default" style="">
<content>COS</content>
</control_layout>
<control_layout id="Q1_tresc" layout="default" style="">
<content>A | B</content>
</control_layout>
<control_open id="Q1_data" length="25" lines="1" mask=".*" name="Q1_data | ConceptSelect" require="true"
results="true" style="display:none;">
<content/>
</control_open>
<control_multi id="Q1_dis" itemlimit="0" layout="vertical" name="Q1_dis" random="false" require="false"
results="true" rotation="false" style="">
<list_item disablerest="true" id="97" name="" style="">
<content>Odmowa</content>
</list_item>
<list_item disablerest="true" id="98" name="" style="">
<content>Nie wiem</content>
</list_item>
</control_multi>
<control_layout id="Q1.js" layout="default" style="">
<content>&lt;script type='text/javascript' src='public/ibisDisabler.js'&gt;&lt;/script&gt;
&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.97','Q1_tresc');
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.97','Q1_data',97);
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.98','Q1_tresc');
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Disabler  --&gt;
&lt;script type='text/javascript'&gt;
setIbisDisabler('Q1_dis.98','Q1_data',98);
&lt;/script&gt;
&lt;!-- End Disabler  --&gt;

&lt;!-- Concept Select  --&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/Selection_sog.css&quot; type=&quot;text/css&quot;&gt;
&lt;script type='text/javascript' src='public/Selection_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
var sel = new Selection({{
textContainerId: &quot;Q1_tresc&quot;,
openContainerId: &quot;Q1_data&quot;,
delimiter: &quot;|&quot;
}});
&lt;/script&gt;
&lt;!-- End ConceptSelect --&gt;</content>
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


# errors
class TestErrors(KreaturaTestCase):
    def test_two_same_caf_numbers(self):
        input_ = """Q S Q1 COS
1 CAF A
1 CAF B"""
        survey = parse(input_)

        self.assertRaises(ValueError, survey.to_xml)


# dimensions
class TestDimensionsStyles(KreaturaTestCase):
    def test_precode(self):
        text_input = """Q S Q1 COS
PRE ' xxx
1 a
2 b"""
        survey = parse(text_input)
        survey.to_xml()
        survey.to_web()
        survey.to_dim()

        dim_exp = '''
    Q1 "COS"
    Categorical [1..1]
    {
        _1 "a",
        _2 "b"

    };
'''

        web_exp = '''    ' xxx
    Q1.Ask()
'''

        self.assertEqual(survey.dim_out, dim_exp)
        self.assertEqual(survey.web_out, web_exp)


# loops
class TestLoop(KreaturaTestCase):
    def test_loop_for_categories(self):
        in_ = """Q G Q1 COS
1 odp a
2 odp b
_
1 stw a [cat]
2 stw b [cat]

FOR CATEGORIES:
1 cat 1
2 cat 2"""

        survey = parse(in_)
        categories = survey.childs[0].childs[0].childs[0].categories

        self.assertEqual(str(categories), '[1,cat 1, 2,cat 2]')


# warnings
class TestWarnings(KreaturaTestCase):
    def test_many_columns_warning(self):
        text_input = """Q S Q1 COS --listcolumn:5
1 a"""

        survey = parse(text_input)
        survey.to_xml()

        expected = "W pytaniu Q1 wskazana liczba kolumn ma być większa niż 3. Nie za szeroko?"
        self.assertEqual(expected, survey.warnings[0])


if __name__ == "__main__":
    KreaturaTestCase.main()

