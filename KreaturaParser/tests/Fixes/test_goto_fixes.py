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
left: left_end
right: right_end
_
01 A
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        #print(etree.tostring(survey.xml, pretty_print=True))

        got = etree.tostring(survey.xml)
        want = '''  <survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
	 sliderOpts = {{
		  value: 0,
		  min: 1,
		  max: 10,
		  step: 1,
		  animate:&quot;slow&quot;,
		  orientation: 'horizontal'
	 }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

&lt;/script&gt;
</content>
          </control_layout>
        </question>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>
'''.format(ct)
        self.assertXmlEqual(got, want)

    def test_sliders_with_ran(self):
        input_ = """Q SLIDERS Q1 COS --ran
left: left_end
right: right_end
_
01 A
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        #print(etree.tostring(survey.xml, pretty_print=True))

        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
	 sliderOpts = {{
		  value: 0,
		  min: 1,
		  max: 10,
		  step: 1,
		  animate:&quot;slow&quot;,
		  orientation: 'horizontal'
	 }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

&lt;/script&gt;

&lt;script type='text/javascript' src='public/rotate_tables.js'&gt;&lt;/script&gt;
&lt;!-- get the file from https://github.com/rkorzen/ibisjs
     optionally uncomment the line bellow (only for tests - never for production!!)
--&gt;
&lt;!--
&lt;script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'&gt;&lt;/script&gt;
&lt;link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'&gt;
--&gt;</content>
          </control_layout>
        </question>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>
'''.format(ct)
        self.assertXmlEqual(got, want)


    def dtest_sliders_with_hide(self):
        input_ = """Q SLIDERS Q1 COS --ran
left: left_end
right: right_end
_
01 A--hide:$Q1:{0} == "1"
02 B
03 C"""

        survey = parse(input_)
        survey.to_xml()
        ct = survey.createtime
        got = etree.tostring(survey.xml)
        want = '''<survey SMSComp="false" createtime="{0}" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000">
    <block id="Default" name="" quoted="false" random="false" rotation="false">
      <page hideBackButton="false" id="Q1_p" name="">
        <question id="Q1" name="">
          <control_layout id="Q1.labelka" layout="default" style="">
            <content>COS</content>
          </control_layout>
          <control_table id="Q1_01_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_stmnt" layout="default" style="">
                  <content>A</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_01" mask=".*" name="Q1_01 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_01_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:01 == "1"]]></hide>
          </control_table>
          <control_table id="Q1_02_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_stmnt" layout="default" style="">
                  <content>B</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_02" mask=".*" name="Q1_02 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_02_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:02 == "1"]]></hide>
          </control_table>
          <control_table id="Q1_03_table" random="false" rotation="false" rrdest="row" style="">
            <row forcestable="true" style="">
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_stmnt" layout="default" style="">
                  <content>C</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_left" layout="default" style="">
                  <content>left: left_end</content>
                </control_layout>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_number float="false" id="Q1_03" mask=".*" name="Q1_03 | COS" require="true" results="true" style="">
                  <content></content>
                </control_number>
              </cell>
              <cell colspan="1" forcestable="false" rowspan="1" style="">
                <control_layout id="Q1_03_table_right" layout="default" style="">
                  <content>right: right_end</content>
                </control_layout>
              </cell>
            </row>
            <hide><![CDATA[$Q1:03 == "1"]]></hide>
          </control_table>
          <control_layout id="Q1.js" layout="default" style="">
            <content>&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/css/ui-lightness/jquery-ui-1.8.9.custom.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/slider/slider.css&quot; type=&quot;text/css&quot;&gt;
&lt;link rel=&quot;stylesheet&quot; href=&quot;public/custom.css&quot; type=&quot;text/css&quot;&gt;

&lt;script type='text/javascript' src='public/slider/js/jquery-ui-1.8.9.custom.min.js'&gt;&lt;/script&gt;

&lt;script type='text/javascript' src='public/slider/slider.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
 sliderOpts = {{
      value: 0,
      min: 1,
      max: 10,
      step: 1,
      animate:&quot;slow&quot;,
      orientation: 'horizontal'
 }};
new IbisSlider(&quot;Q1_01&quot;, sliderOpts);
new IbisSlider(&quot;Q1_02&quot;, sliderOpts);
new IbisSlider(&quot;Q1_03&quot;, sliderOpts);

&lt;/script&gt;

&lt;script type='text/javascript' src='public/rotate_tables.js'&gt;&lt;/script&gt;
&lt;!-- get the file from https://github.com/rkorzen/ibisjs
     optionally uncomment the line bellow (only for tests - never for production!!)
--&gt;
&lt;!--
&lt;script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'&gt;&lt;/script&gt;
&lt;link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'&gt;
--&gt;

</content>
          </control_layout>
        </question>
      </page>
    </block>
    <vars></vars>
    <procedures>
      <procedure id="PROC" shortdesc=""></procedure>
    </procedures>
  </survey>
'''.format(ct)

        self.assertXmlEqual(got, want)