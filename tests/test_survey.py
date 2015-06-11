from elements import Survey, Block
from lxml import etree
from tests.testing_tools import KreaturaTestCase

__author__ = 'KorzeniewskiR'


class TestSurvey(KreaturaTestCase):
    def test_append(self):
        surv1 = Survey()
        surv1.childs.append('A')

        surv2 = Survey()
        surv2.append('A')

        self.assertEqual(surv1, surv2)

    def test_add_to_parent(self):
        """Uzycie metody add_to_parent powinno dać ten sam efekt, co ręczne dodawanie"""

        surv = Survey()
        b1, b2, b3 = Block('B1'), Block('B2'), Block('B3')
        b3.parent_id = 'B2'

        surv.append(b1)
        b1.childs.append(b2)
        surv.add_to_parent(b3)

        e_surv = Survey()
        e_b1, e_b2, e_b3 = Block('B1'), Block('B2'), Block('B3')
        e_b3.parent_id = "B2"

        e_surv.append(e_b1)
        e_b1.childs.append(e_b2)
        e_b2.childs.append(e_b3)

        self.assertEqual(surv, e_surv)

    def test_survey_attributes(self):
        """Pusty element Survey ma trochę atrybutów stałych (domyślnych) i jeden zmienny (createtime)"""
        got = Survey()
        epoch_time = got.createtime
        got.to_xml()
        got = etree.tostring(got.xml)
        want = ('''<survey SMSComp="false"
                           createtime="{}"
                           creator="CHANGEIT"
                           exitpage=""
                           layoutid="ShadesOfGray"
                           localeCode="pl"
                           name="CHANGEIT"
                           sensitive="false"
                           showbar="false"
                           time="60000"></survey>'''.format(epoch_time))

        self.assertXmlEqual(got, want)

    def test_build_xml(self):
        """Metoda to_xml wywoływana jest takż na dzieciach

        Tak naprawdę to ten test trreba by umieścić w innym miejscu
        """

        surv = Survey()
        epoch_time = surv.createtime  # czesc zmienna - musze wstawic ten czas do expected

        # Dodajemmy 2 zagnieżdzone bloki. Blok B1 zawiera B2
        surv.append(Block('B1'))
        surv.childs[0].childs.append(Block('B2'))

        surv.to_xml()
        xml_expc = etree.fromstring('''<survey SMSComp="false"
                           createtime="{}"
                           creator="CHANGEIT"
                           exitpage=""
                           layoutid="ShadesOfGray"
                           localeCode="pl"
                           name="CHANGEIT"
                           sensitive="false"
                           showbar="false"
                           time="60000">
                           <block id="B1" name="" quoted="false" random="false" rotation="false">
                           <block id="B2" name="" quoted="false" random="false" rotation="false"/>
                           </block></survey>'''.format(epoch_time))
        self.assertXmlEqual(etree.tostring(surv.xml), etree.tostring(xml_expc))

