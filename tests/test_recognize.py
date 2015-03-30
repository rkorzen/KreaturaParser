from unittest import TestCase
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

    def test_block_error(self):
        line = 'B B0 B1 -rot'
        result = recognize(line)
        self.assertEqual(None, result)

    def test_ran_rot_error(self):
        line = 'B B0 B1 --rot --ran'
        result = recognize(line)
        self.assertEqual(None, result)

    def test_block_to_many_parents(self):
        line = 'B B0 B1 B2 B3'
        result = recognize(line)
        self.assertEqual(None, result)


class TestPageRecognize(TestCase):

    def test_simple_page(self):
        line = "P P0"
        result = recognize(line)
        self.assertEqual("PAGE", result)

    def test_page_with_hide(self):
        line = 'P P0 --hide:$A1:{0} == "1"'
        result = recognize(line)
        self.assertEqual("PAGE", result)

    def test_page_with_rot(self):
        """Może z czasem ta rotacja bedzie potrzebna"""
        line = 'P P0 --rot --hide:$A1:{0} == "1"'
        result = recognize(line)
        self.assertEqual(None, result)


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


class TestSwitchRecognize(TestCase):
    def test_switch(self):
        line = "_"
        self.assertEqual("SWITCH", recognize(line))

    def test_switch_with_spaces(self):
        line = "_  "
        self.assertEqual("SWITCH", recognize(line))

    def test_switch_double__(self):
        line = "__  "
        self.assertEqual(None, recognize(line))


class TestPrecodeRecognize(TestCase):
    def test_simple_precode(self):
        line = 'PRE $Q1="1";$Q2="2"'
        self.assertEqual("PRECODE", recognize(line))


class TestPostcodeRecognize(TestCase):
    def test_simple_precode(self):
        line = 'POST $Q1="1";$Q2="2"'
        self.assertEqual("POSTCODE", recognize(line))

class TestStatementRecognize(TestCase):
    """kafeterie stwierdzen i odpowiedzi"""

    def test_simple_statement_just_number(self):
        line = "1"
        self.assertEqual("STATEMENT", recognize(line))

    def test_simple_statement_just_word(self):
        line = "coś"
        self.assertEqual("STATEMENT", recognize(line))

    def test_simple_statement_num_word_slash(self):
        line = "97 nie wiem/trudno powiedzieć"
        self.assertEqual("STATEMENT", recognize(line))

    def test_simple_statement_num_word_backslash(self):
        line = "97 nie wiem\trudno powiedzieć"
        self.assertEqual("STATEMENT", recognize(line))

    def test_simple_statement_num_dot_word_backslash(self):
        line = "97.d nie wiem\trudno powiedzieć"
        self.assertEqual("STATEMENT", recognize(line))

    def test_num_dot_c(self):
        line = '97.c inne'
        self.assertEqual("STATEMENT", recognize(line))

    def test_hide(self):
        line = '1 cos --hide:$A1:1 == "1"'
        self.assertEqual("STATEMENT", recognize(line))

    def test_wrong_call_two_hides(self):
        line = '97.c nie wiem\trudno powiedzieć --hide:$A1:1 == "1" --hide:$A1:1 == "1"'
        self.assertEqual(None, recognize(line))
