__author__ = 'korzen'
from BeautifulSoup import BeautifulSoup
from collections import OrderedDict



last_block =  None

class Survey():
    def __init__(self):
        self.blocks = OrderedDict()

    def print_tree(self):
        out = ''
        for key in self.blocks:
            block = self.blocks[key]
            level = check_tree_level(self.blocks, block.parent, 0)
            if block.has_child(self.blocks):
                end = '_'
            else:
                end = ''
            out += '\t'*(level) + key + '\n'
            try:
                for child in block.childs:
                    out += '\t'*(level+1) + 'child: ' + child + '\n'
                    for question in block.childs[child].questions:
                        q = block.childs[child].questions[question]
                        out += '\t'*(level+2) + 'question: ' + q.id +', '+ q.typ + '\n'
            except AttributeError:
                pass
        return out

class Block():
    def __init__(self):
        self.parent = None
        self.id = None
        self.childs = OrderedDict()

    def add_child(self, child):
        self.childs[child.id] = child

    def has_child(self):
        if len(self.childs) > 0:
            return True
        else:
            return False

def print_tree_2(block, level=0):
    out = ''
    if block.has_child():
        level += 1
        for key in block.childs:
            out +='\t'*level + key + 'lvl: ' + str(level) +'\n'
            out += print_tree_2(block.childs[key], level)
    else:
        level = 0
    return out

class Page():
    def __init__(self, id=None, parent=None):
        self.id = id
        self.parent = parent
        self.childs = OrderedDict()

    def add_question(self, q):
        self.childs[q.id] = q


class Question(object):
    def __init__(self, id=None, typ=None, polecenie=None):
        self.id = id
        self.typ = typ
        self.polecenie = polecenie
        self.kafeteria = []
        self.statements = []
        self.childs = ()


def parser(text):
    survey = Block()
    text = text.splitlines()
    for line in text:
        if line.startswith('B '):
            line_tmp = line.split(' ')
            id = line_tmp[1]
            b = Block()
            b.id = id
            b.typ = "block"
            try:
                parent = line_tmp[2]
                last_block.add_child(b)
            except IndexError:
                survey.add_child(b)

            last_block = b

        if line.startswith('P '):
            line_tmp = line.split(' ')
            id = line_tmp[1]
            p = Page(id, last_block.id)
            last_block.add_child(p)
            last_page_id = id

        if line.startswith('Q '):
            line_tmp = line.split(' ')
            id = line_tmp[2]
            typ = line_tmp[1]
            polecenie = line_tmp[3]
            q = Question(id, typ, polecenie)
            try:
                last_block.childs[last_page_id].add_question(q)
            except:
                # musze strone utworzyc:
                page_id = q.id + '_p'
                p = Page(page_id)
                p.add_question(q)
                last_block.add_child(p)
    return survey
    #print(elements)


def check_tree_level(elements, parent_id, level):

    if parent_id is not None:
        level += 1 + check_tree_level(elements, elements[parent_id].parent, level)
    else:
        level = 0
    return level






if __name__ == "__main__":
    text = """B B0
P P1_p
Q S P1 pytnie single
1 a

B B1 B0
Q O Q1 Cos

B B2 B1

B B3 B0

B B4

B B5

B B6 B5
"""
    text = '''B B1
B B2 B1
B B3 B1
B B4 B1
B B5
'''

    s = parser(text)
    print(print_tree_2(s))
