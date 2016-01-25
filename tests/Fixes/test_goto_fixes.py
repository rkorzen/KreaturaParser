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


class TestFix4(KreaturaTestCase):
    def test_sliders(self):
        input_ = """Q SLIDERS Q1 COS
cokolwiek
_
01 A
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        print(survey.createtime)

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
  <page id="Q1_p" hideBackButton="false">
    <precode></precode>
    <postcode></postcode>
    <question id="Q1_p.Q1" name="">
<control_layout id="Q1_p.Q1.label1" layout="default" style="">
<content>COS</content>
</control_layout>
<control_table id="Q1_p.Q1.table1" random="false" rotation="true" rrdest="row" style="">

    <row forcestable="false" style="">
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_1_txt0" layout="default" style="">
    <content>01 A</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_1_txt1" layout="default" style="">
    <content>Lewy koniec</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_number float="false" id="Q1_1" mask=".*" name="Q1_1 01 A" require="true" results="true" style="">
    <content/>
    </control_number>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_layout id="Q1_1_txt2" layout="default" style="">
    <content>Prawy koniec</content>
    </control_layout>
    </cell>
    </row>

    <row forcestable="false" style="">
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_2_txt0" layout="default" style="">
    <content>02 B</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_2_txt1" layout="default" style="">
    <content>Lewy koniec</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_number float="false" id="Q1_2" mask=".*" name="Q1_2 02 B" require="true" results="true" style="">
    <content/>
    </control_number>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_layout id="Q1_2_txt2" layout="default" style="">
    <content>Prawy koniec</content>
    </control_layout>
    </cell>
    </row>

    <row forcestable="false" style="">
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_3_txt0" layout="default" style="">
    <content>03 C</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="true" rowspan="1" style="">
    <control_layout id="Q1_3_txt1" layout="default" style="">
    <content>Lewy koniec</content>
    </control_layout>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_number float="false" id="Q1_3" mask=".*" name="Q1_3 03 C" require="true" results="true" style="">
    <content/>
    </control_number>
    </cell>
    <cell colspan="1" forcestable="false" rowspan="1" style="">
    <control_layout id="Q1_3_txt2" layout="default" style="">
    <content>Prawy koniec</content>
    </control_layout>
    </cell>
    </row>

</control_table>
<control_layout id="Q1_p.Q1.label2" layout="default" style="">
<content>&lt;link rel="stylesheet" href="public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css" type="text/css"&gt;
&lt;link rel="stylesheet" href="public/slider/slider.css" type="text/css"&gt;
&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
     sliderOpts = {
          value: 0,
          min: 1,
          max: 5,
          step: 1,
          animate:"slow",
          orientation: 'horizontal'
     };
new IbisSlider("Q1_1", sliderOpts);new IbisSlider("Q1_2", sliderOpts);new IbisSlider("Q1_3", sliderOpts);
&lt;/script&gt;</content>
</control_layout>
</question>
  </page>


                          </block>
                        <vars/>
                        <procedures>
                        <procedure id="PROC" shortdesc=""/>
                        </procedures>
                    </survey>'''.format(survey.createtime)
        self.assertXmlEqual(got, want)


    def test_sliders_with_hide(self):
        input_ = """Q SLIDERS Q1 COS
cokolwiek
_
01 A --hide:$Z4a:{0}=="1"
02 B
03 C"""