# coding: utf-8
import datetime
from lxml import etree
from collections import OrderedDict
import re

from unittest import TestCase
from doctest import Example
from lxml.doctestcompare import LXMLOutputChecker

def show_attr(element):
    """Drukuje atrybuty"""

    out = ""
    attrs = element.__dict__

    for key in attrs.keys():
        if attrs[key] is None:
            value = "None"
        elif attrs[key] == "":
            value = '""'
        else:
            value = attrs[key]
        out += "{0} = {1}\n".format(key, value)

    out = sorted(out.splitlines())

    return out


def find_parent(blocks, parent_id):
    """Szuka bloku o zadanym parent_id"""
    for block in blocks:
        if block.id == parent_id:
            return block
        else:
            b = find_parent(block.childs, parent_id)
            if b:
                return b


def find_parent(container, el_id):
    """Szuka bloku o zadanym parent_id"""
    print(container)
    if container.childs:
        childs_id = [c.id for c in container.childs]
        #print(childs_id)
        if el_id in childs_id:
            #print("Found ", el_id, " in ", container.childs)
            return container.id
        else:
            for c in container.childs:
                x = find_parent(c, el_id)
                if x is not None:
                    return x
    else:
        #print(container.id, "has no childs")
        pass


def find_by_id(parent, child_id):
    """
    szuka elementu o podanym id i go zwraca

    :param parent: Survey or Block or Page or something with childs <list> attribute
    :param child_id: child id

    """

    if parent.id == child_id:
        return parent
    else:
        if parent.childs:
            for child in parent.childs:
                r = find_by_id(child, child_id)
                if r:
                    return r


def build_precode(precode, tag, technique="ibis"):
    """Designed to build precode, postcode or hide - elements with CDATA"""

    if technique == "ibis":
        is_inside_if = False
        prec = etree.Element(tag)
        text = precode.split(';')

        # pobieżna walidacja
        # czy ilość if else i endif jest taka sama
        count_ifs = [x.startswith('if') for x in text].count(True)
        count_elses = [x.startswith('else') for x in text].count(True)
        count_endifs = [x.startswith('endif') for x in text].count(True)
        # print(count_ifs, count_elses, count_endifs)
        if count_ifs is not count_elses or count_ifs is not count_endifs:
            raise ValueError('Liczba if, else, endif nie zgadza się')

        for i, t in enumerate(text):
            t = t.strip()

            if t.startswith('if'):
                is_inside_if = True
            if t.startswith('endif'):
                is_inside_if = False

            if not t.startswith('if') and not t.startswith('else') and not t.startswith('endif') and is_inside_if:
                text[i] = '  ' + text[i]
        text = '\n'.join(text)

        prec.text = etree.CDATA(text)
    else:
        prec = precode.split(';')
        prec = '\n'.join(prec)
    return prec


def clean_labels(text):
    """
    ma czyścić labelki ze znaczników html

    cos <img src='public/cos.jpg' alt='cos'> -> cos
    """
    import re
    tags_re = re.compile('(<(\S+?)>|<(\S+)\s.*?>)')

    # na wypadek, gdyby niektóre tagi trzeba bylo zostawic
    # tags = ('br', 'sub', 'sup', 'cotamjeszczechcesz')
    tags = ()

    def tags_filter(matchobj):
        matched = matchobj.groups()[1]
        matched = matched if matched else matchobj.groups()[2]

        return matchobj.group(0) if matched in tags else ''

    tekst_bez_znacznikow = tags_re.sub(tags_filter, text)
    return tekst_bez_znacznikow


def wersjonowanie_plci(text, method="ibis"):
    if method == "ibis":
        dict_ = OrderedDict()
        dict_['Pan(i)'] = '#SEX_M#'
        dict_['Pan/i'] = '#SEX_M#'
        dict_['Pan(ni)'] = "#SEX_M"
        dict_['Pan/Pani'] = '#SEX_M#'
        dict_['Pana(i)'] = '#SEX_D#'
        dict_['Pana(-i)'] = '#SEX_D#'
        dict_['Pana(ni)'] = '#SEX_D#'
        dict_['Pana/i'] = '#SEX_D#'
        dict_['Pana/Pani'] = '#SEX_D#'
        dict_['Panu(i)'] = '#SEX_C#'
        dict_['Panu/i'] = '#SEX_C#'
        dict_['Pani(u)'] = '#SEX_C#'
        dict_['Pana(ią)'] = '#SEX_B#'
        dict_['Panem(ią)'] = '#SEX_N#'
        dict_['Panem(nią)'] = '#SEX_N#'
        dict_['y(a)'] = '#END_Y#'
        dict_['(a)'] = '#END_A#'
        dict_['em/am'] = '#END_EM#'
        dict_['em(am)'] = '#END_EM#'
        dict_['e(am)'] = "#END_EM#"
        dict_['by/aby'] = '#END_A#by'
        dict_['Panu/Pani'] = '#SEX_C#'
    elif method == "dim":
        dict_ = OrderedDict()
        dict_['Pan(i)'] = '{#Pan}'
        dict_['Pan/i'] = '{#Pan}'
        dict_['Pan(ni)'] = '{#Pan}'
        dict_['Pan/Pani'] = '{#Pan}'
        dict_['Pana(i)'] = '{#Pana}'
        dict_['Pana(-i)'] = '{#Pana}'
        dict_['Pana/i'] = '{#Pana}'
        dict_['Pana(ni)'] = '{#Pana}'
        dict_['Pana/Pani'] = '{#Pana}'
        dict_['Panu(i)'] = '{#Panu}'
        dict_['Panu/i'] = '{#Panu}'
        dict_['Pani(u)'] = '{#Panu}'
        dict_['Panu/Pani'] = '{#Panu}'
        dict_['Pana(ią)'] = '{#PanaPania}'
        dict_['Panem(ią)'] = '{#Panem}'
        dict_['Panem(nią)'] = '{#Panem}'
        dict_['y(a)'] = '{#y}'
        dict_['y/a'] = '{#y}'
        dict_['(a)'] = '{#a}'
        dict_['em/am'] = '{#em}'
        dict_['em(am)'] = '{#em}'
        dict_['e(am)'] = '{#em}'
        dict_['by/aby'] = '{#a}by'
        dict_['ął(ęła)'] = '{#al}'

    for key in dict_.keys():
        text = text.replace(key, dict_[key])
    return text


def filter_parser(input_):
    """
    filter_parser stara się tłumaczyć ibisowe filtry precodu/postcodu na routingu dim.


    """

    if input_.strip().startswith("'"):  # dim style
        return '    ' + input_
    else:       # ibis translations
        data = input_.split(';')

        for x in data:
            data[data.index(x)] = data[data.index(x)].strip()

        try:
            goto = data.index('goto next')
        except ValueError as e:
            goto = False

        data = data[0].replace('if', '').replace('(', '').replace(')', '').replace('$', '')
        warunek = data.strip()
        filtr_pattern = re.compile('([\w\d_]+):(\d*) == "(\d)"')
        warunek = filtr_pattern.match(warunek)

        if not goto:
            return False

        if not warunek:
            return False

        warunek = warunek.groups()
        id_ = warunek[0]
        answer_position = warunek[1]
        flaga = warunek[2]

        # rozpoznane patterny zwraca do uzupelnienia
        if (goto == 1 and flaga == "0") or (goto == 2 and flaga == "1"):
            return '\n    if {0}.ContainsAny("x{1}") then {{}}.Ask()\n\n'.format(id_, answer_position)
        else:
            return '\n    if not {0}.ContainsAny("x{1}") then {{}}.Ask()\n\n'.format(id_, answer_position)


def clean_line(line):
    """:rtype : string

    Funkcja ma za zadanie oczyść linię ze zbędnych odstępów, tabulacji
    ? Ewentualne znaki & zamienić powinna na &amp;

    """
    line = line.replace("\t", ' ')
    line = " ".join(line.split())
    line = line.strip()
    line = line.replace('&', '&amp;')
    line = line.replace('&amp;amp;', '&amp;')

    return line


def print_tree(survey):
    """Wizualizuje drzewo elementow"""
    out = []

    def element_tree(element, level=0):
        out.append('\t'*level + element.id)
        if not element.childs:
            pass
        else:
            for child in element.childs:
                element_tree(child, level+1)

    bloki = survey.childs
    for blok in bloki:
        element_tree(blok)

    out = '\n'.join(out)
    print(out)
    return out


def make_caf_to_dim(cafeteria, tabs=0, prov_letter = 'x'):
    """:returns string
    :param cafeteria: cafeteria or statements list
    :param tabs: level of indent
    """

    out = ""
    ile = len(cafeteria)
    for caf in cafeteria:

        if '--i' in caf.content:
            caf.content = caf.content.replace('--i',"")
            caf.content = '<i>' + caf.content.strip() + '</i>'

        if '--b' in caf.content:
            caf.content = caf.content.replace('--b',"")
            caf.content = '<b>' + caf.content + '</b>'

        if '|' in caf.content:
            caf.content = caf.content.split('|')
            caf.img = caf.content[1]
            caf.content = caf.content[0]

        if "--use:" in caf.content:
            list_ = caf.content.split('--use:')[1]
            out += "    "*tabs + r"{0} use \\.{0} -".format(list_)
        elif caf.deactivate:
            out += '    '*tabs + '- "{}" DK'.format(caf.content)
        else:
            out += '    '*tabs + prov_letter + caf.id + ' "' + caf.content + '"'


        if caf.other:
            out += ' other'

        if caf.img:
            out += r'''
            labelstyle(
                Image = "images\{0}",
                ImagePosition = "ImageOnly"
            )'''.format(caf.img)

        if cafeteria.index(caf) == ile-1:
            out += '\n'
        else:
            out += ",\n"

    return out


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def unix_creation_time(dt):
    """Czas utworzenia - ms epoch time - coś analogicznego do tworzonego w kreaturze"""
    return int(unix_time(dt) * 1000)


# region testing tools
class KreaturaTestCase(TestCase):

    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        # 2048 - PARSE_HTML
        # 4096 - PARSE_XML
        # 8192 - NOPARSE_MARKUP
        if not checker.check_output(want, got, 4096):
            message = checker.output_difference(Example("", want), got, 4096)
            raise AssertionError(message)

    def assertTxtEqual(self, expected, actual):
        msg = "'" + actual + "' != '" + expected + "'"
        assert expected == actual, msg

# end region