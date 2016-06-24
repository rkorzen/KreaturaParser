# coding: utf-8
from sdl.tools import KreaturaTestCase
from sdl.parsers import Patterns, block_parser, page_parser,  question_parser, cafeteria_parser, program_parser
from sdl.elements import Block, Page, Question, Cafeteria


class TestPatterns(KreaturaTestCase):

    def test_goto_pattern(self):
        line1 = "--goto:Q1_p"
        line2 = "1 A --goto:Q1_p"
        line3 = "1 A --goto:Q1_p --hide:cos"
        line4 = "1 A--goto:Q1_p--hide:cos"
        line5 = "1 A--goto: Q1_p--hide:cos"
        pattern = Patterns.goto_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1) and self.assertEqual(r1.group(0), "Q1_p")
        self.assertIsNotNone(r2) and self.assertEqual(r2.group(0), "Q1_p")
        self.assertIsNotNone(r3) and self.assertEqual(r3.group(0), "Q1_p")
        self.assertIsNotNone(r4) and self.assertEqual(r4.group(0), "Q1_p")
        self.assertIsNotNone(r5) and self.assertEqual(r5.group(0), "Q1_p")


    def test_hide_pattern(self):
        line1 = 'A --hide: $P4B:{0} == "1"'
        line2 = 'A--hide:$P4B:{0} == "1"'
        pattern = Patterns.hide_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)

        expected = '$P4B:{0} == "1"'

        self.assertEqual(expected, r1.group(1))
        self.assertEqual(expected, r2.group(1))

    def test_cafeteria_pattern(self):
        line1 = 'A--hide:$P4B:{0} == "1"'
        line2 = 'A --hide:$P4B:{0} == "1"'
        line3 = '1 coś coś --hide:$A1:{0} == "1"'
        line4 = '-1 coś'
        line5 = 'A --hide:$P4B:{0} == "1" --so'
        pattern = Patterns.caf_pattern

        r1 = pattern.match(line1)
        r2 = pattern.match(line2)
        r3 = pattern.match(line3)
        r4 = pattern.match(line4)
        r5 = pattern.match(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNotNone(r4)
        self.assertIsNotNone(r5)


    def test_screenout_pattern(self):
        line1 = "cos--so"
        line2 = "cos --so"
        line3 = "cos\t --so"
        line4 = "cos - -so"
        line5 = "cos -so"
        pattern = Patterns.screen_out_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNone(r4)
        self.assertIsNone(r5)


    def test_goto_next_pattern(self):
        line1 = "cos--gn"
        line2 = "cos --gn"
        line3 = "cos\t --gn"
        line4 = "cos - -gn"
        line5 = "cos -gn"
        pattern = Patterns.goto_next_pattern

        r1 = pattern.search(line1)
        r2 = pattern.search(line2)
        r3 = pattern.search(line3)
        r4 = pattern.search(line4)
        r5 = pattern.search(line5)

        self.assertIsNotNone(r1)
        self.assertIsNotNone(r2)
        self.assertIsNotNone(r3)
        self.assertIsNone(r4)
        self.assertIsNone(r5)


class TestBlockParser(KreaturaTestCase):
    def test_simple_block(self):
        line = "B B0"
        result = block_parser(line)
        expected = Block("B0")

        self.assertEqual(result, expected)

    def test_block_with_parent(self):
        line = "B B0 B1"
        result = block_parser(line)
        expected = Block("B0")
        expected.parent_id = "B1"
        self.assertEqual(result, expected)

    def test_block_with_hide(self):
        line = 'B B0 --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        self.assertEqual(result, expected)

    def test_block_with_rot_parent_and_hide(self):
        line = 'B B0 B1 --rot --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        expected.rotation = True
        expected.parent_id = "B1"
        self.assertEqual(result, expected)

    def test_block_with_ran_parent_and_hide(self):
        line = 'B B0 B1 --ran --hide:$A1="1"'
        result = block_parser(line)
        expected = Block("B0")
        expected.hide = '$A1="1"'
        expected.random = True
        expected.parent_id = "B1"
        self.assertEqual(result, expected)


class TestPageParser(KreaturaTestCase):

    def test_page_parser(self):
        line = "P P0"
        result = page_parser(line)
        expected = Page("P0")
        self.assertEqual(result, expected)

    def test_page_parser_with_hide(self):
        line = 'P P0 --hide: $A1:97 == "1"'
        result = page_parser(line)
        expected = Page("P0")
        expected.hide = '$A1:97 == "1"'
        self.assertEqual(result, expected)

    def test_page_with_parent(self):
        line = "P P0 --parent:MAIN"
        got = page_parser(line)

        want = Page('P0')
        want.parent_id = "MAIN"

        self.assertEqual(got, want)


class TestQuestionParser(KreaturaTestCase):
    def test_simple_single_question_parser(self):
        line = "Q S Q0 Treść"
        expected = Question("Q0")
        expected.typ = "S"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_multi_question_parser(self):
        line = "Q M Q0 Treść"
        expected = Question("Q0")
        expected.typ = "M"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_layout_question_parser(self):
        line = "Q L Q0 Treść"
        expected = Question("Q0")
        expected.typ = "L"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_question_parser(self):
        line = "Q G Q0 Treść"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_old_question_parser(self):
        line = "Q SDG Q0 Treść"
        expected = Question("Q0")
        expected.typ = "SDG"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_basket_question_parser(self):
        line = "Q B Q0 Treść"
        expected = Question("Q0")
        expected.typ = "B"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_basket_old_question_parser(self):
        line = "Q LHS Q0 Treść"
        expected = Question("Q0")
        expected.typ = "LHS"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_table_question_parser(self):
        line = "Q T Q0 Treść"
        expected = Question("Q0")
        expected.typ = "T"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_numeric_question_parser(self):
        line = "Q N Q0 Treść"
        expected = Question("Q0")
        expected.typ = "N"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_parser(self):
        line = "Q O Q0 Treść"
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_with_size_parser(self):
        line = "Q O90_4 Q0 Treść"
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        expected.size = ['90', '4']
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_question_with_size_and_hide_parser(self):
        line = 'Q O90_4 Q0 Treść--hide:$A1="1"'
        expected = Question("Q0")
        expected.typ = "O"
        expected.content = "Treść"
        expected.size = ['90', '4']
        expected.hide = '$A1="1"'
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_rotation(self):
        line = "Q G Q0 Treść --rot"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.rotation = True
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_random(self):
        line = "Q G Q0 Treść --ran"
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.random = True
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_grid_with_random_and_hide(self):
        line = 'Q G Q0 Treść --ran--hide:$A1:1 == "1"'
        expected = Question("Q0")
        expected.typ = "G"
        expected.content = "Treść"
        expected.random = True
        expected.hide = '$A1:1 == "1"'
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_single_with_parent(self):
        line = "Q S Q1 --p:Q0 Treść"
        expected = Question("Q1")
        expected.typ = "S"
        expected.content = "Treść"
        expected.parent_id = "Q0"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_open_with_deactivate(self):
        line = "Q O Q1 TRESC --dk:Nie wiem"
        expected = Question("Q1")
        expected.typ = "O"
        expected.content = "TRESC"
        expected.dontknow = "Nie wiem"
        result = question_parser(line)
        self.assertEqual(expected, result)

    def test_mutli_rot_list_lz(self):
        input_ = "Q M M13 Czy w Pana(i) gospodarstwie domowym jest? --rot --list:dobra --lz:1"
        expected = Question("M13")
        expected.typ = "M"
        expected.content = "Czy w Pana(i) gospodarstwie domowym jest? --list:dobra --lz:1"
        expected.rotation = True
        result = question_parser(input_)
        self.assertEqual(expected, result)


class TestStatementParser(KreaturaTestCase):

    def test_slash(self):
        line = "Nie wiem/trudno powiedzieć"
        expected = Cafeteria()
        expected.content = "Nie wiem/trudno powiedzieć"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_backslash(self):
        line = r"Nie wiem\trudno powiedzieć"
        expected = Cafeteria()
        expected.content = r"Nie wiem\trudno powiedzieć"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_nr(self):
        line = "1 cos"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_minus(self):
        line = "-1 cos"
        expected = Cafeteria()
        expected.id = "-1"
        expected.content = "-1 cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_just_minus(self):
        line = "-1"
        expected = Cafeteria()
        expected.id = "-1"
        expected.content = "-1"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_polish_signs(self):
        line = "1 coś coś"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_no_id(self):
        line = "coś coś"
        expected = Cafeteria()
        expected.content = "coś coś"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_deacticate(self):
        line = "96.d coś coś"
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "coś coś"
        expected.deactivate = True
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_other(self):
        line = "96.c coś coś"
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "coś coś"
        expected.other = True
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_hide(self):
        line = '1 coś coś --hide:$A1:{0} == "1"'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.hide = '$A1:{0} == "1"'
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_screenout(self):
        line = '1 coś coś --so'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.screenout = True
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_with_gotonext(self):
        line = '1 coś coś --gn'
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "coś coś"
        expected.gotonext = True
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_all_possible(self):
        line = '96.d Procter&Gamble --hide: $A1:{0} == "1" --so'
        expected = Cafeteria()
        expected.id = "96"
        expected.content = "Procter&Gamble"
        expected.hide = '$A1:{0} == "1"'
        expected.deactivate = True
        expected.screenout = True

        result = cafeteria_parser(line)[0]

        self.assertEqual(expected, result)

    def test_screeonout_info(self):
        line = '1 cos --so'

        expected = Cafeteria()
        expected.id = '1'
        expected.content = 'cos'
        expected.screenout = True

        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_screeonout_info_2(self):
        line = '1 a --so'

        expected = Cafeteria()
        expected.id = '1'
        expected.content = 'a'
        expected.screenout = True

        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_tabs(self):
        line = "1   cos"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_dot(self):
        line = "1.   cos"
        expected = Cafeteria()
        expected.id = "1"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_colon(self):
        line = "9: cos"
        expected = Cafeteria()
        expected.id = "9"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)

    def test_cafeteria_with_semicolon(self):
        line = "9;cos"
        expected = Cafeteria()
        expected.id = "9"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)


    def test_cafeteria_with_comma(self):
        line = "9,cos"
        expected = Cafeteria()
        expected.id = "9"
        expected.content = "cos"
        result = cafeteria_parser(line)[0]
        self.assertEqual(expected, result)


class TestProgramParser(KreaturaTestCase):

    def test_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_two_empty_container(self):
        input_ = "B B0\nBEGIN PROGRAM\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nEND PROGRAM"

        expected = "B B0\n\nB B1\n"
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_two_not_empty_container_without_print(self):
        input_ = "B B0\nBEGIN PROGRAM\nA=1\nEND PROGRAM\nB B1\nBEGIN PROGRAM\nB=2\nEND PROGRAM"

        expected = """B B0

B B1
"""
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_for_loop(self):
        input_ = """B B0
BEGIN PROGRAM
def func():
    out = ""
    for i in range(2):
        out += '''P P{0}
'''.format(i)
    return out
xxx = func()
END PROGRAM"""

        expected = """B B0
P P0
P P1
"""
        result = program_parser(input_)

        self.assertEqual(expected, result)

    def test_loop_over_list(self):
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
        result = program_parser(input_)
        expected = """B B0

Q O Q1_1 Co myślisz o osobie o imieniu Ania

Q O Q1_2 Co myślisz o osobie o imieniu Hania

Q O Q1_3 Co myślisz o osobie o imieniu Lena

"""

        self.assertEqual(expected, result)


if __name__ == '__main__':
    KreaturaTestCase.main()
