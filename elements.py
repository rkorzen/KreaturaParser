from lxml import etree
from tools import build_precode, find_parent

import datetime


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_creation_time(dt):
    """Czas utworzenia - ms epoch time - coś analogicznego do tworzonego w kreaturze"""
    return int(unix_time(dt) * 1000)


class SurveyElements:
    """Base of survey structures/elements"""

    def __init__(self, id_):
        self.id = id_
        # self.precode = ''
        self.precode = False
        # self.postcode = ''
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


class Survey:
    """
    Survey contain childs
    Survey have s method to add a block element to his parent
    """

    def __init__(self):
        self.childs = []
        self.id = False   # just for a case... and for find_by_id function
        self.createtime = unix_creation_time(datetime.datetime.now())
        self.xml = False

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
        self.xml.set('SMSComp', "false")
        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)

        vars_ = etree.Element('vars')
        self.xml.append(vars_)

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
        self.xml.set('quoted', 'false')
        self.xml.set('random', 'false')
        self.xml.set('rotation', 'false')

        if self.quoted:
            self.xml.set('quoted', 'true')

        if self.random:
            self.xml.set('random', 'true')

        if self.rotation:
            self.xml.set('rotation', 'true')

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)


class Page(SurveyElements):
    """Page element."""

    def __init__(self, id_):
        SurveyElements.__init__(self, id_)
        self.hideBackButton = False
        # self.postcode = ""

    def to_xml(self):
        """xml representation of Page element"""
        # self.postcode = ""
        self.xml = etree.Element('page')
        self.xml.set('id', self.id)
        self.xml.set('hideBackButton', 'false')
        self.xml.set('name', '')
        # print(self.precode)
        if self.hideBackButton:
            self.xml.set('hideBackButton', 'true')

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            # ustawiam postcode dziecka na to co mamy
            child.postocde = self.postcode

            # metoda xml tworzy atrybut xml z odpowiednią zawartoscia
            # jej wywołanie wpływa jednak także na .postcode
            # przekazywany jest on aż do poziomu kafeterii i potem idzie w góre
            child.to_xml()

            # aktualizuję postcode strony tym  co zebrane w głębi
            self.postcode = child.postcode
            self.xml.append(child.xml)

        # print("jestem tu: ". self.postcode)
        if self.postcode:
            # drukowanie postcodu do xmla ma sens tylko w przypadku stron i bloków
            # w tym przypadku chodzi o postcode strony tworzony na podstawie
            # jego dzieci
            postcode = etree.Element('postcode')
            postcode.text = etree.CDATA(self.postcode)

            self.xml.append(postcode)


class Question(SurveyElements):
    """Question"""
    def to_xml(self):
        """xml representation of Question element"""

        # TODO: tutaj duużo do zrobienia - wszystkie typy
        self.xml = etree.Element('question')
        self.xml.set('id', self.id)
        self.xml.set('name', '')

        layout = ControlLaout(self.id + '.labelka')
        layout.content = self.content
        layout.to_xml()
        self.xml.append(layout.xml)

        # region control_layout
        if self.typ is "L":
            # layout = ControlLaout(self.id + '.labelka')
            # layout.content = self.content
            # layout.to_xml()
            # self.xml.append(layout.xml)

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
            # layout = ControlLaout(self.id+'.labelka')
            # layout.content = self.content
            # layout.to_xml()
            # self.xml.append(layout.xml)

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
            # layout = ControlLaout(self.id + '.labelka')
            # layout.content = self.content
            # layout.to_xml()
            # self.xml.append(layout.xml)

            single = ControlSingle(self.id)
            single.cafeteria = self.cafeteria
            single.name = self.id + ' | ' + self.content
            single.postcode = self.postcode
            single.to_xml()
            self.postcode = single.postcode

            self.xml.append(single.xml)
        # endregion

        # region control_multi
        if self.typ == "M":
            # layout = ControlLaout(self.id + '.labelka')
            # layout.content = self.content
            # layout.to_xml()
            # self.xml.append(layout.xml)

            multi = ControlMulti(self.id)
            multi.cafeteria = self.cafeteria
            multi.name = self.id + ' | ' + self.content
            multi.postcode = self.postcode
            multi.to_xml()
            self.postcode = multi.postcode

            self.xml.append(multi.xml)
        # endregion

        # region control_number
        if self.typ == "N":
            if self.cafeteria:
                for nr, caf in enumerate(self.cafeteria):
                    if not caf.id:
                        id_suf = '_' + str(nr+1)
                    else:
                        id_suf = '_' + str(caf.id)

                    open_ = ControlNumber(self.id + id_suf)
                    open_.name = self.id + id_suf + ' | ' + caf.content
                    if self.size:
                        open_.size = self.size
                    open_.to_xml()
                    self.xml.append(open_.xml)
            else:
                open_ = ControlNumber(self.id)
                open_.name = self.id + ' | ' + self.content
                if self.size:
                    open_.size = self.size
                open_.to_xml()
                self.xml.append(open_.xml)
        # endregion


class Control:
    def __init__(self, id_, **kwargs):
        self.id = id_
        self.xml = False
        self.tag = None
        self.layout = False
        self.style = ""
        self.require = "true"
        self.hide = False
        self.rotation = 'false'
        self.random = 'false'
        self.name = None
        self.results = 'true'
        self.cafeteria = []
        self.statements = []
        self.xml = ""
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def to_xml(self):
        self.xml = etree.Element(self.tag)
        self.xml.attrib['id'] = self.id

        if self.layout:
            self.xml.attrib['layout'] = self.layout
            self.xml.set('layout', self.layout)
        else:
            self.xml.set('layout', 'default')
        if self.style:
            self.xml.set('style', self.style)
        else:
            self.xml.set('style', '')


class ControlLaout(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.tag = 'control_layout'
        if 'content' in kwargs:
            self.content = kwargs['content']
        else:
            self.content = False

    def to_xml(self):
        Control.to_xml(self)

        content = etree.Element('content')
        if self.content:
            content.text = self.content

        self.xml.append(content)


class ControlOpen(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
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
        # example: <control_open id="Q1" length="25" line="1" mask=".*" require="true" results="true" rotation="false"
        # style="" name="Q1 COS"/>
        self.xml = etree.Element(self.tag)
        self.xml.set('id', self.id)
        self.xml.set('length', self.size[0])
        self.xml.set('lines', self.size[1])
        self.xml.set('mask', self.mask)
        self.xml.set('name', self.name)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('style', self.style)

        content = etree.Element('content')
        if self.content:
            content.text = self.content

        self.xml.append(content)


class ControlSingle(Control):
    # example: <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 Kryss av:" random="false"
    # require="true" results="true" rotation="false" style="">
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.tag = 'control_single'

        if not self.layout:
            self.layout = 'vertical'
        self.itemlimit = "0"

        # wartości nadpisane
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

    def to_xml(self):

        self.xml = etree.Element(self.tag)
        self.xml.set('id', self.id)
        self.xml.set('itemlimit', self.itemlimit)
        self.xml.set('layout', self.layout)

        # self.name powinno być ustawione w question przed wywołaniem metody to_xml()
        self.xml.set('name', self.name)
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
        if self.cafeteria:

            for caf in self.cafeteria:
                list_item = Cafeteria()
                list_item.id = caf.id
                list_item.content = caf.content
                list_item.to_xml()

                self.xml.append(list_item.xml)
                if caf.screenout:
                    self.postcode += """
if (${0}:{1} == "1")
#OUT = "1"
goto KONKURS
else
endif
""".format(self.id, caf.id)
        else:
            raise ValueError("Brak kafeterii w pytaniu: ", self.id)


class ControlMulti(ControlSingle):
    # example: <control_single id="Q1" itemlimit="0" layout="vertical" name="Q1 Kryss av:" random="false"
    # require="true" results="true" rotation="false" style="">
    def __init__(self, id_, **kwargs):
        ControlSingle.__init__(self, id_, **kwargs)
        self.tag = 'control_multi'


class ControlNumber(Control):
    # example min: <control_number float="false" id="Q2" mask=".*" name="" require="true" results="true" style="">
    # example max: <control_number float="true" id="Q2" mask=".*" max="99.0" maxsize="2" min="1.0" name=""
    # require="true" results="true" style="">

    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_, **kwargs)
        self.float = "false"
        self.mask = ".*"
        # self.content = ""
        # self.require = 'true'
        # self.results = 'true'
        # self.style = ""

        self.max = None
        self.maxsize = None
        self.min = None

    def to_xml(self):
        # self.name = self.id + ' | ' + self.content
        self.xml = etree.Element('control_number')
        self.xml.set('id', self.id)
        self.xml.set('float', self.float)
        self.xml.set('mask', self.mask)
        self.xml.set('name', self.name)
        self.xml.set('require', self.require)
        self.xml.set('results', self.results)
        self.xml.set('style', self.style)

        if self.max:
            self.xml.set('max', self.max)
        if self.min:
            self.xml.set('min', self.min)
        if self.maxsize:
            self.xml.set('maxsize', self.maxsize)

        # w sumie chyna nigdy nie użyłem wartości wpisanej domyślnie w control_number
        # gdyby była taka potrzeba.. to coś tu trzeba będzie zmienic
        content = etree.SubElement(self.xml, 'content')


class Cafeteria:
    """List element - to np cafeteria, statements"""

    def __init__(self, **kwargs):
        self.tag = 'list_item'
        self.id = None
        self.content = ""
        self.hide = None
        self.deactivate = False
        self.other = False
        self.screenout = False
        self.gotonext = False
        self.xml = None

        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])

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


class CallsForScripts:
    def __init__(self, id_, typ_, **kwargs):
        self.id = id_
        self.typ = typ_

    def js_table(self):
        """Xml kontrolki z wywołaniem skryptów tabelki js"""
        control = '''<control_layout id="{0}tableJs" layout="default" style="">
<content>
&lt;link rel="stylesheet" href="public/tables.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/tables.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;

jQuery(document).ready(function(){{
// ustawienia:

// wspolny prefix kontrolek
// zwróć uwagę by nie zaczynało się tak id page/question
t = new Table("{0}_");

// jeśli ma być transpozycja, odkomentuj poniższe
//t.transposition();

// jeśli nie ma być randoma, zakomentuj to
t.shuffle();

t.print();
}});
&lt;/script&gt;

&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;
</content>
</control_layout>'''.format(self.id)

        return etree.fromstring(control)