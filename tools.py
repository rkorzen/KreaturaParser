# coding: utf-8
from lxml import etree
from collections import OrderedDict
import re

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
        # print(text)
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


def wersjonowanie_plci(text):
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

    for key in dict_.keys():
        text = text.replace(key, dict_[key])
    return text


def wersjonowanie_plci_dim(text):
    dict_ = OrderedDict()
    dict_['Pan(i)'] = '{#Pan}'
    dict_['Pan/i'] = '{#Pan}'
    dict_['Pan(ni)'] = '{#Pan}'
    dict_['Pan/Pani'] = '{#Pan}'
    dict_['Pana(i)'] = '{#Pana}'
    dict_['Pana(-i)'] = '{#Pana}'
    dict_['Pana/i'] = '{#Pana}'
    dict_['Pana(ni)'] = '{#Pana}'
    dict_['Pana/Pani'] =  '{#Pana}'
    dict_['Panu(i)'] =  '{#Panu}'
    dict_['Panu/i'] =  '{#Panu}'
    dict_['Pani(u)'] =  '{#Panu}'
    dict_['Panu/Pani'] =  '{#Panu}'
    dict_['Pana(ią)'] = '{#PanaPania}'
    dict_['Panem(ią)'] =  '{#Panem}'
    dict_['Panem(nią)'] =  '{#Panem}'
    dict_['y(a)'] =  '{#y}'
    dict_['y/a'] =  '{#y}'
    dict_['(a)'] =  '{#a}'
    dict_['em/am'] =  '{#em}'
    dict_['em(am)'] =  '{#em}'
    dict_['e(am)'] =  '{#em}'
    dict_['by/aby'] =  '{#a}by'
    dict_['ął(ęła)'] = '{#al}'

    for key in dict_.keys():
        #print(key, type(key), dict_[key])
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
