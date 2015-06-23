__author__ = 'KorzeniewskiR'

from unittest import TestCase
from doctest import Example
from lxml.doctestcompare import LXMLOutputChecker


class KreaturaTestCase(TestCase):

    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        # 2048 - PARSE_HTML
        # 4096 - PARSE_XML
        # 8192 - NOPARSE_MARKUP
        if not checker.check_output(want, got, 4096):
            message = checker.output_difference(Example("", want), got, 4096)
            raise AssertionError(message)
