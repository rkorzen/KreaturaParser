from unittest import TestCase
from kparser import parse
from elements import Block, Page, Question, Cafeteria


class TestParse(TestCase):

    def test_only_block(self):
        text_input = """B B0"""
        result = parse(text_input)
        block = Block("B0")
        expected = [block]
        self.assertEqual(expected, result)

    def test_block_page(self):
        text_input = """B B0
P P0"""
        result = parse(text_input)
        block = Block("B0")
        page = Page("P0")
        block.childs.append(page)
        expected = [block]
        self.assertEqual(expected, result)

    def test_only_page(self):
        text_input = "P P0"
        page = Page("P0")
        block = Block("Default")
        block.childs.append(page)
        expected = [block]
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
        expected = [block]
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

        expected = [block]
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
        expected = [block]
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
        expected = [block]
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
        expected = [block]
        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_block_with_precode_postcode(self):
        text_input = "B B0\nPRE x\nPOST y"
        block = Block("B0")
        block.precode = "x"
        block.postcode = "y"
        expected = [block]
        result = parse(text_input)
        self.assertEqual(expected, result)

    def test_page_with_precode_postcode(self):
        text_input = "P P0\nPRE x\nPOST y"
        page = Page("P0")
        page.precode = "x"
        page.postcode = "y"

        block = Block("Default")
        block.childs.append(page)
        expected = [block]
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

        expected = [block]

        result = parse(text_in)
        # print(result[0].childs[0].childs)
        self.assertEqual(expected, result)