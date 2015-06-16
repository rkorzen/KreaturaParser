from lxml import etree


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


def build_precode(precode, tag):
    """Designed to build precode, postcode or hide - elements with CDATA"""

    is_inside_if = False
    prec = etree.Element(tag)

    text = precode.split(';')

    # pobieżna walidacja
    # czy ilość if else i endif jest taka sama

    count_ifs = [x.startswith('if') for x in text].count(True)
    count_elses = [x.startswith('else') for x in text].count(True)
    count_endifs = [x.startswith('endif') for x in text].count(True)

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

    return prec
