__author__ = 'KorzeniewskiR'

from unittest import TestCase
from doctest import Example
from lxml.doctestcompare import LXMLOutputChecker

class KreaturaTestCase(TestCase):

    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        if not checker.check_output(want, got, 4096):
            message = checker.output_difference(Example("", want), got, 4096)
            raise AssertionError(message)
