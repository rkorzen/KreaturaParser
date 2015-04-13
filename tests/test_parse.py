from unittest import TestCase
from kparser import parse
from elements import Block, Page, Question, Cafeteria, Survey


class TestParse(TestCase):

    def test_only_block(self):
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

    def test_only_page(self):
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

    def test_only_question(self):
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

    def test_block_question_single_1_el(self):
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

    def test_block_question_table_1_el_1_st(self):
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
        question.statements.append(stw)

        page.childs.append(question)
        block.childs.append(page)

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_block_with_precode_postcode(self):
        text_input = "B B0\nPRE x\nPOST y"
        block = Block("B0")
        block.precode = "x"
        block.postcode = "y"

        survey = Survey()
        survey.append(block)
        expected = survey

        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_page_with_precode_postcode(self):
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
        # print(result[0].childs[0].childs)
        self.assertEqual(expected, result)

    def test_with_empty_program(self):
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

    def test_with_loop(self):
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

    def test_block_with_parrent(self):
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
        expected = survey

        result = parse(input_)

        # for page in result[0].childs:
        #     for question in page.childs:
        #         print("question: ", question.id)
        #         for key in question.__dict__:
        #             if question.__dict__[key]:
        #                 print(key, question.__dict__[key])
        #
        # print('\n\nexpected')
        # for page in expected[0].childs:
        #     for question in page.childs:
        #         print("question: ", question.id)
        #         for key in question.__dict__:
        #             if question.__dict__[key]:
        #                 print(key, question.__dict__[key])


        self.assertEqual(expected, result)

    def test_block_nesting(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    out = ''
    for i in range(5):
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

        expected = survey.append(b0)

        result = parse(input_)

        self.assertEqual(expected, result)

    def test_block_nesting_one_parent(self):
        input_ = """B B0

BEGIN PROGRAM
def func():
    out = ''
    for i in range(5):
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

        b0.childs.append(b1)
        b0.childs.append(b2)
        b0.childs.append(b3)
        b0.childs.append(b4)

        survey = Survey()
        survey.append(b0)
        expected = survey

        result = parse(input_)

        self.assertEqual(expected, result)