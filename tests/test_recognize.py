from unittest import TestCase, main
from kparser import recognize


class TestBlockRecognize(TestCase):

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


class TestPageRecognize(TestCase):

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


class TestQuestionRecoginize(TestCase):

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


class TestSwitchRecognize(TestCase):
    def test_switch(self):
        line = "_"
        self.assertEqual("SWITCH", recognize(line))

    def test_switch_with_spaces(self):
        line = "_  "
        self.assertEqual("SWITCH", recognize(line))

    def test_switch_double__(self):
        line = "__  "
        self.assertEqual("SWITCH", recognize(line))


class TestPrecodeRecognize(TestCase):
    def test_simple_precode(self):
        line = 'PRE $Q1="1";$Q2="2"'
        self.assertEqual("PRECODE", recognize(line))


class TestPostcodeRecognize(TestCase):
    def test_simple_precode(self):
        line = 'POST $Q1="1";$Q2="2"'
        self.assertEqual("POSTCODE", recognize(line))


class TestCafeteriaRecognize(TestCase):
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
        self.assertEqual('CAFETERIA', recognize(line))
        self.assertEqual('CAFETERIA', recognize(line2))
        self.assertEqual('CAFETERIA', recognize(line3))
        self.assertEqual('CAFETERIA', recognize(line4))
        self.assertEqual('CAFETERIA', recognize(line5))

class TestBlankRecognize(TestCase):
    def test_blank_line(self):
        line = ""
        self.assertEqual("BLANK", recognize(line))


class TestCommentRecognize(TestCase):

    def test_comment_line(self):
        input_ = "// this is a comment"
        self.assertEqual("COMMENT", recognize(input_))

if __name__ == '__main__':
    main()
