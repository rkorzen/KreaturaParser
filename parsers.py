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
    r = re.compile("^Q (S|M|L|N|O|LHS|SDG|T|B|G){1}([0-9]+_[0-9]+){0,1} ([\w_.]+) (.*)$").match(line)

    question = Question(r.group(3))  # id
    question.typ = r.group(1)

    if r.group(2):                   # size
        size = r.group(2).split('_')
        question.size = size

    question.content = r.group(4)    # content

    if " --hide:" in line:           # hide
        question.hide = line.split(" --hide:")[1]
        question.content = question.content.split(' --hide:')[0]

    if " --rot" in line:
        question.rotation = True
        question.content = question.content.replace(' --rot', '')

    if " --ran" in line:
        question.random = True
        question.content = question.content.replace(' --ran', '')


    return question


def list_element_parser(line):
    line = line.strip()

    pattern = re.compile("^(\d+|\d+\.) (.*)( --hide:.*){0,1}$")

    if " --hide:" in line:
        hide = line.split(' --hide:')[1]
        line = line.split(' --hide:')[0]



