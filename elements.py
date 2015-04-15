def find_parent(blocks, parent_id):
    for block in blocks:
        if block.id == parent_id:
            return block
        else:
            b = find_parent(block.childs, parent_id)
            if b:
                return b


class SurveyElements():
    """Base of survey structures/elements"""

    def __init__(self, id_):
        self.id = id_
        self.precode = False
        self.postcode = False
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
                self.content == other.content
                )


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
        self.childs.append(block)

    def add_to_parent(self, block):
        parent = find_parent(self.childs, block.parent_id)
        if parent:
            parent.childs.append(block)
        else:
            raise Exception("Wrong parent id")


class Block(SurveyElements):
    pass


class Page(SurveyElements):
    pass


class Question(SurveyElements):
    """Question"""
    pass


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