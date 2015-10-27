from unittest import main
from KreaturaParser.kparser import parse, print_tree
from KreaturaParser.elements import Block, Page, Question, Cafeteria, Survey
from lxml import etree
from KreaturaParser.tests.testing_tools import KreaturaTestCase


class TestFix3(KreaturaTestCase):
    def test_goto(self):
        line = """Q S Q1 COS
A --goto: A4_p

Q S Q2 COS
A"""
        survey = parse(line)
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
                                                 <control_single id="Q1"
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
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
<precode>
<![CDATA[if ($Q1:1 == "1")
    goto A4_p
else
endif]]>
</precode>
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                 </list_item>
                                                 </control_single>
                                       </question>
                                 </page>

                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)

    def test_2_cond_in_hide(self):
        input_ = '''Q S Q2 COS
1 A --hide:$Q1:{0} == "1" || $Q1a:{0} == "1"
2 B'''
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
                                 <page id="Q2_p"
                                       hideBackButton="false"
                                       name="">
                                       <question id="Q2"
                                                 name="">
                                                 <control_layout id="Q2.labelka"
                                                                 layout="default"
                                                                 style="">
                                                                 <content>COS</content>
                                                 </control_layout>
                                                 <control_single id="Q2"
                                                                 itemlimit="0"
                                                                 layout="vertical"
                                                                 name="Q2 | COS"
                                                                 random="false"
                                                                 require="true"
                                                                 results="true"
                                                                 rotation="false"
                                                                 style="">
                                                                 <list_item id="1" name="" style="">
                                                                    <content>A</content>
                                                                    <hide><![CDATA[$Q1:1 == "1" || $Q1a:1 == "1"]]></hide>
                                                                 </list_item>
                                                                 <list_item id="2" name="" style="">
                                                                    <content>B</content>
                                                                    <hide><![CDATA[$Q1:2 == "1" || $Q1a:2 == "1"]]></hide>
                                                                 </list_item>

                                                 </control_single>
                                       </question>
                                 </page>
                          </block>
                        <vars></vars>
                        <procedures>
                          <procedure id="PROC" shortdesc=""></procedure>
                        </procedures>
                    </survey>'''.format(survey.createtime)

        self.assertXmlEqual(got, want)
