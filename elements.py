from lxml import etree
from tools import build_precode, find_parent

import datetime


def unix_time(dt):

    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch

    return delta.total_seconds()

def unix_creatiom_time(dt):
    return int(unix_time(dt) * 1000)

class SurveyElements():
    """Base of survey structures/elements"""

    def __init__(self, id_):
        self.id = id_
        #self.precode = ''
        self.precode = False
        #self.postcode = ''
        self.postcode = ""
        self.rotation = False
        self.random = False
        self.hide = False
        self.childs = []
        self.parent_id = False
        self.typ = False
        self.cafeteria = []
        self.statements = []
        self.size = []
        self.content = False
        self.dontknow = False
        self.xml = False

    def __eq__(self, other):
        return (self.id == other.id and
                self.parent_id == other.parent_id and
                self.precode == other.precode and
                self.postcode == other.postcode and
                self.rotation == other.rotation and
                self.random == other.random and
                self.hide == other.hide and
                self.childs == other.childs and
                self.typ == other.typ and
                self.cafeteria == other.cafeteria and
                self.statements == other.statements and
                self.size == other.size and
                self.content == other.content and
                self.dontknow == other.dontknow

                )

    def set_precode(self):
        """Set precode of element"""
        if self.precode:  # jeśli element ma precode
            try:
                prec = build_precode(self.precode, 'precode')
                self.xml.append(prec)

            except ValueError as e:
                raise ValueError("Błąd w precode elementu {0}, {1}".format(self.id, e))


class Survey():
    """
    Survey contain childs
    Survey have s method to add a block element to his parent
    """

    def __init__(self):
        self.childs = []
        self.id = False   # just for a case... and for find_by_id function
        self.createtime = unix_creatiom_time(datetime.datetime.now())

    def __eq__(self, other):
        return self.childs == other.childs and self.id == other.id

    def append(self, block):
        """Add child to self.childs list"""
        self.childs.append(block)

    def add_to_parent(self, block):
        """
        Add child to his parent. Parent is nested somewhere in survey childs
        If there is not element with parent_id Exception is thrown.
        """
        parent = find_parent(self.childs, block.parent_id)
        if parent:
            parent.childs.append(block)
        else:
            # TODO: some other exception type?
            raise Exception("Wrong parent id")

    def to_xml(self):
        """survey xml"""
        # TODO: opcjonalnie - procedury, zmienne
        self.xml = etree.Element('survey')
        self.xml.set('createtime', str(self.createtime))
        self.xml.set('creator', "CHANGEIT")
        self.xml.set('exitpage', "")
        self.xml.set('layoutid', "ShadesOfGray")
        self.xml.set('localeCode', "pl")
        self.xml.set('name', "CHANGEIT")
        self.xml.set('sensitive', "false")
        self.xml.set('showbar', "false")
        self.xml.set('time', "60000")
        self.xml.set('SMSComp',"false")
        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)

        vars = etree.Element('vars')
        self.xml.append(vars)

        procedures = etree.Element('procedures')
        procedure = etree.Element('procedure')
        procedure.set('id', 'PROC')
        procedure.set('shortdesc', '')
        procedures.append(procedure)


        self.xml.append(procedures)



class Block(SurveyElements):
    """Block element."""

    def __init__(self, id_):
        SurveyElements.__init__(self, id_)
        self.quoted = False

    def to_xml(self):
        """xml representation of Block element"""
        self.xml = etree.Element('block')
        self.xml.set('id', self.id)
        self.xml.set('name', '')

        if self.quoted:
            self.xml.set('quoted', 'true')
        else:
            self.xml.set('quoted', 'false')

        if self.random:
            self.xml.set('random', 'true')
        else:
            self.xml.set('random', 'false')

        if self.rotation:
            self.xml.set('rotation', 'true')
        else:
            self.xml.set('rotation', 'false')

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)


class Page(SurveyElements):
    """Page element."""

    def __init__(self, id_):
        SurveyElements.__init__(self, id_)
        self.hideBackButton = False


    def to_xml(self):
        """xml representation of Page element"""
        self.postcode = ""
        self.xml = etree.Element('page')
        self.xml.set('id', self.id)

        if self.hideBackButton:
            self.xml.set('hideBackButton', 'true')
        else:
            self.xml.set('hideBackButton', 'false')

        self.xml.set('name', '')

        self.set_precode()  # SurveyElements method

        for child in self.childs:

            child.postocde = self.postcode
            child.to_xml()

            self.postcode = child.postcode
            self.xml.append(child.xml)

        if self.postcode:
            print("tututut")
            postcode = etree.Element('postcode')
            postcode.text = etree.CDATA(self.postcode)
            self.xml.append(postcode)

class Question(SurveyElements):
    """Question"""
    def to_xml(self):
        """xml representation of Question element"""
        print(self.postcode)
        # TODO: tutaj duużo do zrobienia - wszystkie typy
        self.xml = etree.Element('question')
        self.xml.set('id', self.id)
        self.xml.set('name', '')

        # region control_layout
        if self.typ is "L":
            layout = ControlLaout(self.id + '.labelka')
            layout.content = self.content
            layout.to_xml()
            self.xml.append(layout.xml)

            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    if not caf.id:
                        id_suf = '_' + str(nr+1)
                    else:
                        id_suf = '_' + str(caf.id)
                    layout_ = ControlLaout(self.id + id_suf + '_txt')
                    layout_.content = caf.content
                    layout_.to_xml()
                    self.xml.append(layout_.xml)

        # endregion

        # region control_open
        if self.typ is "O":
            # dodaję kontrolkę tekstową z pytaniem
            layout = ControlLaout(self.id+'.labelka')
            layout.content = self.content
            layout.to_xml()
            self.xml.append(layout.xml)

            # dodaję kontrolkę/kontrolki open
            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    if not caf.id:
                        id_suf = '_' + str(nr+1)
                    else:
                        id_suf = '_' + str(caf.id)

                    open_ = ControlOpen(self.id + id_suf)
                    open_.name = self.id + id_suf + ' | ' + caf.content
                    if self.size:
                        open_.size = self.size
                    open_.to_xml()
                    self.xml.append(open_.xml)
            else:
                open_ = ControlOpen(self.id)
                open_.name = self.id + ' | ' + self.content
                if self.size:
                    open_.size = self.size
                open_.to_xml()
                self.xml.append(open_.xml)
        # endregion

        # region control_single
        if self.typ == "S":
            layout = ControlLaout(self.id + '.labelka')
            layout.content = self.content
            layout.to_xml()

            self.xml.append(layout.xml)

            single = ControlSingle(self.id)
            single.cafeteria = self.cafeteria
            single.content = self.content
            single.postcode = self.postcode
            single.to_xml()

            self.xml.append(single.xml)
        # endregion

        # region control_multi
        if self.typ == "M":
            layout = ControlLaout(self.id + '.labelka')
            layout.content = self.content
            layout.to_xml()

            self.xml.append(layout.xml)

            single = ControlMulti(self.id)
            single.cafeteria = self.cafeteria
            single.content = self.content
            single.to_xml()

            self.xml.append(single.xml)
        # endregion


class Control():
    def __init__(self, id, **kwargs):
        self.id = id
        self.xml = False
        self.tag = None
        self.layout = False
        self.style = False

        if 'require' in kwargs:
            self.require = kwargs['require']
        else:
            self.require = "true"

        if 'hide' in kwargs:
            self.hide = kwargs['hide']
        else:
            self.hide = False

        if 'rotation' in kwargs:
            self.rotation = kwargs['rotation']
        else:
            self.rotation = 'false'

        if 'random' in kwargs:
            self.random = kwargs['randomize']
        else:
            self.random = 'false'

    def to_xml(self):
        self.xml = etree.Element(self.tag)
        self.xml.attrib['id'] = self.id
        # el_control = ET.Element(self.type)
        # el_control.attrib['id'] = self.id
        # el_control.attrib['length'] = self.length
        # el_control.attrib['line'] = self.line
        # el_control.attrib['mask'] = self.mask
        # el_control.attrib['require'] = self.require
        # el_control.attrib['results'] = self.results
        # el_control.attrib['rotation'] = self.rotation

        if self.layout:
            self.xml.attrib['layout'] = self.layout
            self.xml.set('layout', self.layout)
        else:
            self.xml.set('layout', 'default')
        if self.style:
            self.xml.set('style', self.style)
        else:
            self.xml.set('style', '')

        # el_control.attrib['name'] = self.name


class ControlLaout(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_,**kwargs)
        self.tag = 'control_layout'
        if 'content' in kwargs:
            self.content = kwargs['content']
        else:
            self.content = False

    def to_xml(self):
        Control.to_xml(self)
        self.xml.attrib['id']

        content = etree.Element('content')
        if self.content:
            content.text = self.content

        self.xml.append(content)


class ControlOpen(Control):
    def __init__(self, id, **kwargs):
        Control.__init__(self, id, **kwargs)
        self.tag = 'control_open'

        # default values:
        self.content = False
        self.require = 'true'
        self.size = ['25', '1']
        self.mask = '.*'
        self.results = 'true'
        self.style = ''
        self.name = self.id

        # wartości nadpisane
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def to_xml(self):
        # example: <control_open id="Q1" length="25" line="1" mask=".*" require="true" results="true" rotation="false" style="" name="Q1 COS"/>
        self.xml = etree.Element(self.tag)
        self.xml.set('id', self.id)
        self.xml.set('length', self.size[0])
        self.xml.set('lines', self.size[1])
        self.xml.set('mask', self.mask)
        self.xml.set('name', self.name)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        #self.xml.set('rotation', self.rotation)
        self.xml.set('style', self.style)

        content = etree.Element('content')
        if self.content:
            content.text = self.content

        self.xml.append(content)


class ControlSingle(Control):
    # example: <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 Kryss av:" random="false" require="true" results="true" rotation="false" style="">
    def __init__(self, id_, **kwargs):
        self.id = id_
        self.tag = 'control_single'

        # wartosci domyślne:
        self.cafeteria = None
        self.content = ""
        self.itemlimit = "0"
        self.layout = 'vertical'

        self.random = "false"
        self.rotation = "false"
        self.style = ""
        self.require = "true"
        self.results = "true"

        # wartości nadpisane
        for key in kwargs:
            if kwargs[key]:
                print('ustawiam', key, kwargs[key])
                setattr(self, key, kwargs[key])

    def to_xml(self):
        self.xml = etree.Element(self.tag)
        self.xml.set('id', self.id)
        self.xml.set('itemlimit', self.itemlimit)
        self.xml.set('layout', self.layout)
        self.xml.set('name', self.id + ' | ' + self.content)
        self.xml.set('random', self.random)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('rotation', self.rotation)
        self.xml.set('style', self.style)

        """Sprawdzenie, czy ma kafeterię zostawiam tutaj. Nie chcę tego robić w init
        ponieważ dopuszczam różne możliwości ustawiania atrybutu:
          + poprzez kwargs
          + poprzez bezpośrednie odwołania
        """
        if not self.cafeteria:
            raise ValueError("Brak kafeterii w pytaniu: ", self.id)

        for caf in self.cafeteria:
            list_item = Cafeteria()
            list_item.id = caf.id
            list_item.content = caf.content
            list_item.to_xml()

            self.xml.append(list_item.xml)
            if caf.screenout:
                self.postcode = self.postcode + """
if (${0}:{1} == "1")
#OUT = "1"
goto KONKURS
else
endif
""".format(self.id, caf.id)

class ControlMulti(ControlSingle):
    # example: <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 Kryss av:" random="false" require="true" results="true" rotation="false" style="">
    def __init__(self, id_, **kwargs):
        ControlSingle.__init__(self, id_, **kwargs)
        self.tag = 'control_multi'


class Cafeteria():
    """List element - to np cafeteria, statements"""

    def __init__(self):
        self.tag = 'list_item'
        self.id = None
        self.content = ""
        self.hide = None
        self.deactivate = False
        self.other = False
        self.screenout = False
        self.gotonext = False

    def __eq__(self, other):
        return(self.id == other.id and
               self.content == other.content and
               self.hide == other.hide and
               self.deactivate == other.deactivate and
               self.other == other.other and
               self.screenout == other.screenout and
               self.gotonext == other.gotonext
               )

    def __repr__(self):
        return str(self.id) + ',' + self.content

    def to_xml(self):
        self.xml = etree.Element('list_item')
        self.xml.set('id', self.id)
        self.xml.set('name', "")
        self.xml.set('style', "")
        content = etree.Element('content')
        content.text = self.content
        self.xml.append(content)


