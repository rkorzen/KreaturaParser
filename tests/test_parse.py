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

    def test_block_question(self):
        text_input = """B B0
Q S Q1 Cos"""
        block = Block("B0")
        page = Page("Q1_p")
        question = Question("Q1")
        question.typ = "S"
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
