import re
from elements import Block, Page, Question, ListElement

def block_parser(line):
    id = line.split(' ', 2)[1]
    block = Block(id)

    parent_pattern = re.compile("(B )([\w._]+)( )([\w._]+).*")
    r = parent_pattern.match(line)
    if r:
        block.parent_id = r.group(4)

    if " --rot" in line:
        block.rotation = True
        line = line.replace(' --rot', '')
    if " --ran" in line:
        block.random = True
        line = line.replace(' --ran', '')
    if " --hide:" in line:
        block.hide = line.split(" --hide:")[1]

    return block


def page_parser(line):
    id = line.split(' ', 2)[1]
    page = Page(id)

    if " --hide:" in line:
        page.hide = line.split(" --hide:")[1]

    return page


def question_parser(line):
    id = line.split(' ', 3)[2]
    typ = line.split(' ', 3)[1]
    question = Question(id)
    question.typ = typ



    if " --hide:" in line:
        question.hide = line.split(" --hide:")[1]

    return question

