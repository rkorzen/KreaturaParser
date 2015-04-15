
def show_attr(element):
    """Drukuje atrybuty"""

    out = ""
    attrs = element.__dict__

    for key in attrs.keys():
        out += "{0} = {1}\n".format(key, attrs[key])

    out = sorted(out.splitlines())


    return out



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

