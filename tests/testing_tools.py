__author__ = 'KorzeniewskiR'

from unittest import TestCase
from doctest import Example
from lxml.doctestcompare import LXMLOutputChecker
# from lxml.doctestcompare import PARSE_HTML, PARSE_XML, NOPARSE_MARKUP
#
# print(PARSE_HTML)
# print(PARSE_XML)
# print(NOPARSE_MARKUP)


class KreaturaTestCase(TestCase):

    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        # 2048 - PARSE_HTML
        # 4096 - PARSE_XML
        # 8192 - NOPARSE_MARKUP
        if not checker.check_output(want, got, 4096):
            message = checker.output_difference(Example("", want), got, 4096)
            raise AssertionError(message)
