__author__ = 'KorzeniewskiR'

from KreaturaParser.kparser import parse


from lxml import etree
from KreaturaParser.tests.testing_tools import KreaturaTestCase


class Test_Fix1(KreaturaTestCase):
    def test_colon_in_cafeteria(self):
        input_ = """Q M Q1 COS
1 A: B
"""
        survey = parse(input_)
        survey.to_xml()

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_multi id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A: B</content>
                                                                 </list_item>
                                                 </control_multi>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_hide_and_space(self):
        input_ = '''Q M Q1 COS
A--hide:$P4B:{0} == "1"'''

        survey = parse(input_)
        survey.to_xml()
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false"
                          createtime="{0}"
                          creator="CHANGEIT"
                          exitpage=""
                          layoutid="ShadesOfGray"
                          localeCode="pl"
                          name="CHANGEIT"
                          sensitive="false"
                          showbar="false"
                          time="60000">
                          <block id="Default"
                                 quoted="false"
                                 random="false"
                                 rotation="false"
                                 name="">
                                 <page id="Q1_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q1"
                                                 name="">
                                                 <control_layout id="Q1.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_multi id="Q1"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q1 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                    <hide><![CDATA[$P4B:1 == "1"]]></hide>
                                                                 </list_item>
                                                 </control_multi>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>

                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)