__author__ = 'korzen'
from bs4 import BeautifulSoup
#from BeautifulSoup4 import BeautifulSoup
from collections import OrderedDict

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
    def __init__(self, id, parent=None):
        self.parent = parent
        self.id = id
        self.childs = OrderedDict()

    def add_child(self, child):
        self.childs[child.id] = child

    def has_child(self):
        if len(self.childs) > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.id

    def __unicode__(self):
        return self.id


    def childs_tree(self, level=0):

        out = ''
        for child in self.childs:
            #print("jestem w pętli for, level = ", level, 'child = ', child)
            out += '\t' * level + child + ' lvl: ' + str(level) +'\n'
            if len(self.childs[child].childs) > 0:
                level += 1
                out += self.childs[child].childs_tree(level)
                level -= 1

        return out

    def add_child_to_parent(self, b):
        for child in self.childs:
            if child == b.parent:
                #print("dodaję do: {0} dziecko {1}".format(child, b))
                self.childs[child].add_child(b)
            else:
                self.childs[child].add_child_to_parent(b)


class Page(Block):

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
    survey = Block('survey')
    text = text.splitlines()
    current_block = None

    for line in text:
        if line.startswith('B '):
            line = line.split()

            block_id = line[1]

            try:
                block_parent_id = line[2]
            except IndexError:
                block_parent_id = None

            b = Block(block_id, block_parent_id)
            if b.parent:
                survey.add_child_to_parent(b)
            else:
                survey.add_child(b)

            current_block = b
            continue

        if line.startswith('P '):
            line = line.split()
            page_id = line[1]
            p = Page(page_id, current_block.id)

            current_block.add_child(p)

            continue
        # if line.startswith('P '):
        #     line_tmp = line.split(' ')
        #     id = line_tmp[1]
        #     p = Page(id, last_block.id)
        #     last_block.add_child(p)
        #     last_page_id = id
        #
        # if line.startswith('Q '):
        #     line_tmp = line.split(' ')
        #     id = line_tmp[2]
        #     typ = line_tmp[1]
        #     polecenie = line_tmp[3]
        #     q = Question(id, typ, polecenie)
        #     try:
        #         last_block.childs[last_page_id].add_question(q)
        #     except:
        #         # musze strone utworzyc:
        #         page_id = q.id + '_p'
        #         p = Page(page_id)
        #         p.add_question(q)
        #         last_block.add_child(p)
    return survey
    #print(elements)


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
P P2
B B3 B1
B B4 B1
B B5
B B6
B B7 B6
B B8 B7
B B9 B8
B B10
B B11 B10
P P1'''

#     text = '''B B1
# B B2 B1
# P P2
# B B3 B1
# B B4 B1
# '''




    s = parser(text)
    #print(s.childs)
    #print(s.childs['B1'].childs)
    print(s.childs_tree())
