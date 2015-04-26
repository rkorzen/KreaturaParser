from lxml import etree
from tools import build_precode, find_parent


class SurveyElements():
    """Base of survey structures/elements"""

    def __init__(self, id_):
        self.id = id_
        self.precode = ''
        self.postcode = ''
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
        if self.precode:  # jeśli element ma precode
            try:
                prec = build_precode(self.precode)
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
        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)


class Block(SurveyElements):
    """Block element."""
    def to_xml(self):
        """xml representation of Block element"""
        self.xml = etree.Element('block')
        self.xml.set('id', self.id)

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)


class Page(SurveyElements):
    """Page element."""
    def to_xml(self):
        """xml representation of Page element"""
        self.xml = etree.Element('page')
        self.xml.set('id', self.id)

        self.set_precode()  # SurveyElements method

        for child in self.childs:
            child.to_xml()
            self.xml.append(child.xml)


class Question(SurveyElements):
    """Question"""
    def to_xml(self):
        """xml representation of Question element"""

        # TODO: tutaj duużo do zrobienia - wszystkie typy
        self.xml = etree.Element('question')
        self.xml.set('id', self.id)

        if self.typ is "O":
            if self.cafeteria:
                for caf in self.cafeteria:
                    pass
            else:

                control = ControlOpen(self.id)
                control.to_xml()

                self.xml.append(control.xml)


class Control():
    def __init__(self, id, **kwargs):
        self.id = id
        self.xml = False
        self.tag = None

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
        # el_control.attrib['style'] = self.style
        # el_control.attrib['name'] = self.name


class ControlLaout(Control):
    def __init__(self, id_, **kwargs):
        Control.__init__(self, id_,**kwargs)
        self.tag = 'control_layout'

    def to_xml(self):
        self.xml.attrib['id']




class ControlOpen(Control):
    def __init__(self, id, **kwargs):
        Control.__init__(self, id, **kwargs)
        self.tag = 'control_open'
        if 'content' in kwargs:
            self.content = kwargs['content']
            self.name = self.id + ' | ' + self.content

        if 'require' in kwargs:
            self.require = kwargs['require']
            if self.require:
                self.require = 'true'
            else:
                self.require = 'false'
        else:
            self.require = 'true'

        if 'size' in kwargs:
            s = kwargs['size']
            s = s.split('_')
            self.length = s[0]
            self.line = s[1]
        else:
            self.length = '25'
            self.line = '1'

    # <control_open id="Q1" length="25" line="1" mask=".*" require="true" results="true" rotation="false" style="" name="Q1 COS"/>
    def to_xml(self):
        control = etree.Element(self.tag)
        control.attrib['id'] = self.id
        self.xml = control

class Cafeteria():
    """List element - to np cafeteria, statements"""

    def __init__(self):
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

    def to_xml(self):
        pass


