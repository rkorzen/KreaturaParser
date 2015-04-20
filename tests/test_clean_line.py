from unittest import TestCase, main
from kparser import clean_line


class TestCleanLine(TestCase):

    def test_double_spaces(self):
        line = "B  B0  "
        self.assertEqual('B B0', clean_line(line))

    def test_tabulation_spaces(self):
        line = "B\tB0  "
        self.assertEqual('B B0', clean_line(line))

    def test_ampersand(self):
        line = "Q S Q1 Procter & gamble  "
        self.assertEqual('Q S Q1 Procter &amp; gamble', clean_line(line))

    def test_switch_with_spaces(self):
        line = "_  "
        self.assertEqual("_", clean_line(line))

if __name__ == '__main__':
    main()