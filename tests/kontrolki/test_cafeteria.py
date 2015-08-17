from lxml import etree

from KreaturaParser.tests import KreaturaTestCase
from elements import Cafeteria

__author__ = 'KorzeniewskiR'


class TestCafeteria(KreaturaTestCase):
    def test_to_xml(self):
        c = Cafeteria()
        c.id = "1"
        c.content = "A"
        c.hide = '$Q1:{0} == "1"'

        c.to_xml()

        got = etree.tostring(c.xml, pretty_print=True)
        want = '''
<list_item id="1" name="" style="">
<content>A</content>
<hide><![CDATA[$Q1:1 == "1"]]></hide>
</list_item>
'''

        self.assertXmlEqual(got, want)

    def test_repr(self):
        c = Cafeteria()
        c.id = '1'
        c.content = 'a'
        self.assertEqual('1,a', str(c))
