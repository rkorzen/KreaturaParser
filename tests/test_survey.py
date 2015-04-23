from unittest import TestCase
from elements import Survey, Block
from lxml import etree
__author__ = 'KorzeniewskiR'


class TestSurvey(TestCase):
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

    def test_build_xml(self):
        """"""
        surv = Survey()
        surv.append(Block('B1'))
        surv.childs[0].childs.append(Block('B2'))
        surv.build_xml()
        xml_expc = etree.fromstring('<survey><block id="B1"><block id="B2"/></block></survey>')
        self.assertEqual(etree.tostring(surv.xml), etree.tostring(xml_expc))