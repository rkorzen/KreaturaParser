

class SurveyElements():
    """Base of survey structures/elements"""
    def __init__(self, id):
        self.id = id
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

    def __eq__(self, other):
        return self.id == other.id and \
               self.parent_id == other.parent_id and \
               self.precode == other.precode and \
               self.postcode == other.postcode and \
               self.rotation == other.rotation and \
               self.random == other.random and \
               self.hide == other.hide and \
               self.childs == other.childs and \
               self.typ == other.typ and \
               self.cafeteria == other.cafeteria and \
               self.statements == other.statements


class Block(SurveyElements):
    pass


class Page(SurveyElements):
    pass


class Question(SurveyElements):
    """Question"""
    pass


class ListElement():
    """List element - to np cafeteria, statements"""
    def __init__(self, id):
        self.id = ""
        self.content = ""
        self.hide = ""