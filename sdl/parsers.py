# coding: utf-8
import re
from .elements import Block, Page, Question, Cafeteria

# TODO: przenieść patterny w jedno miejsce (są używane przynajmniej w dwóch i stamtąd ich używać!)


class Patterns:
    # example: B B1 B0 --ran --hide: $A1:{0} == "1"
    block_pattern = re.compile("^(B)(( )[\w_.]+){1,2}(( --ran)|( --rot))?( --hide:.*)?$")

    # example: P P0 --hide: $A1:{0} == "1"
    # example: P P0 --parent:Q --hide: $A1:97 == "1"
    page_pattern = re.compile("^(P )([\w_.]+)*(([ ])*(--parent:)([\w_.]+))?([ ])*((--hide:)(.*))*$")  # z grupowaniem

    # example: Q O Q1 Coś tam --rot --hide
    question_pattern = re.compile("^Q (S|M|L|N|O|LHS|B|SDG|T|G|SLIDER|SLIDERS|H|R|CS|DEF)([0-9]+_[0-9]+)? [\w_.]+ (.*)$")
    question_pattern_advanced = re.compile("^Q (S|M|L|N|O|LHS|B|SDG|G|B|T|SLIDER|SLIDERS|H|R|CS|DEF)([0-9]+_[0-9]+)? "
                                           "([\w_.]+)( --p:([\w_.]+))? (.*)$")
    precode_pattern = re.compile("^PRE .*$")
    postcode_pattern = re.compile("^POST .*$")
    comment_line_pattern = re.compile("^//.*$")

    #caf_pattern = re.compile("^((-{0,1}\d+)(\.d|\.c)? )?([\w ĄĘĆÓŃŚŹŻąęćóńśźż,.–%\-+\(\)&\\\\/\?!’'„”;:-<>=\"\{}\$\|\[\]\{\}@]+)$")
    caf_pattern = re.compile("^((-{0,1}\d+)(\.d|\.c|.f|\.|;|,|:)?\s*)?(.+)$")
    screen_out_pattern = re.compile("\s*--so")
    goto_next_pattern = re.compile("\s*--gn")

    # example: "" < blank line
    blanck_pattern = re.compile("^$")

    parent_pattern = re.compile("(B )([\w._]+)( )([\w._]+).*")
    #hide_pattern = re.compile("\s*--hide:\s*([/:#\$\[\]\w\d\{\} \";'!=\&\|()-]+)")
    hide_pattern = re.compile("\s*--hide:\s*((.(?!--))*)")
    goto_pattern = re.compile("\s*--goto:\s*([\w_.]+)")
    loop_pattern = re.compile("^FOR CATEGORIES:$")


def block_parser(line):
    """
    :param line: String
    :rtype: Block

    """

    id_ = line.split(' ', 2)[1]
    block = Block(id_)

    # parent_pattern = re.compile("(B )([\w._]+)( )([\w._]+).*")
    parent_pattern = Patterns.parent_pattern
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
    """
    :param line: String
    :rtype: Page

    """
    r = Patterns.page_pattern.match(line)
    parent_id = r.groups()[5]

    id_ = line.split(' ', 2)[1]
    page = Page(id_)
    hide = Patterns.hide_pattern.search(line)
    if hide:
        page.hide = hide.group(1)
        #page.hide = line.split(" --hide:")[1]
    if parent_id:
        page.parent_id = parent_id


    return page


def question_parser(line):
    """
    :param line: String
    :rtype: Question

    """
    try:
        r = Patterns.question_pattern_advanced.match(line)
        question = Question(r.group(3))  # id
        question.typ = r.group(1)

        if r.group(2):                   # size opena
            size = r.group(2).split('_')
            question.size = size

        if r.group(5):
            question.parent_id = r.group(5)

        question.content = r.group(6)    # content
        # hide_pattern = Patterns.hide_pattern
        # hp = hide_pattern.find(question.content)
        #
        # print(hp.groups())

        ''' sprawdzam, czy w treści jest " --dk:"
        jeśli jest to przeczyszczam q.content i ustawian q.dontknow

        jeśli w open jest dontknow to będę dodawać skrypt deaktywacja opena

        '''
        if '--dk:' in question.content:
            tmp = question.content.split(' --dk:')
            question.content = tmp[0]
            if tmp[1].strip():
                question.dontknow = tmp[1].strip()
            else:
                question.dontknow = r"Nie wiem / trudno powiedzieć"

        if "--hide:" in line:           # hide
            question.hide = line.split("--hide:")[1]
            question.content = question.content.split('--hide:')[0]

        if " --rot" in line:
            question.rotation = True
            question.content = question.content.replace(' --rot', '')

        if " --ran" in line:
            question.random = True
            question.content = question.content.replace(' --ran', '')

    except AttributeError as e:
        raise AttributeError(e, line)
    return question


def cafeteria_parser(line, add_id_to_content=False):
    """
    :param line: String
    :rtype: Cafeteria

    """
    add_id_to_content = add_id_to_content

    cafeteria = Cafeteria()
    cafeteria_pattern = Patterns.caf_pattern
    caf = cafeteria_pattern.match(line)

    if caf.group(2):           # id
        cafeteria.id = caf.group(2)

    if not caf.group(2):

        try:
            int(caf.group(4))
            cafeteria.id = caf.group(4)
        except ValueError:
            pass

    if cafeteria.id:
        if int(cafeteria.id) < 0:
            add_id_to_content = True


    if caf.group(4):           # content
        cafeteria.content = caf.group(4)

        if add_id_to_content:
            try:
                int(cafeteria.content)
            except ValueError:
                cafeteria.content = cafeteria.id + ' ' + cafeteria.content

        so = Patterns.screen_out_pattern
        gn = Patterns.goto_next_pattern

        so = so.search(cafeteria.content)
        gn = gn.search(cafeteria.content)
        goto = Patterns.goto_pattern.search(cafeteria.content)
        hide = Patterns.hide_pattern.search(cafeteria.content)

        if so:
            cafeteria.screenout = True
            cafeteria.content = cafeteria.content.replace(so.group(0), "")

        if gn:
            cafeteria.gotonext = True
            cafeteria.content = cafeteria.content.replace(gn.group(0), "")

        if goto:
            cafeteria.goto = goto.group(1)
            cafeteria.content = re.sub(goto.group(0),"",cafeteria.content)

        if hide:
            cafeteria.hide = hide.group(1)
            cafeteria.content = cafeteria.content.replace(hide.group(0), '')

    if caf.group(3) == ".d":   # deactivate
        cafeteria.deactivate = True

    if caf.group(3) == ".c":   # comment
        cafeteria.other = True

    # TODO: usunąć to
    if caf.group(3) == ".f":   # comment
        cafeteria.fixposition = True
        cafeteria.other = True

    return cafeteria, add_id_to_content


def program_parser(input_):
    """text - > text

    Sprawdza czy w tekscie są bloki
    BEGIN PROGRAM

    END PROGRAM

    zwraca text z wykonanymi blokami programów.
    To będą najczęściej jakieś pętle typu:
    out = ""
    for i in range(x):
        out += "B B{}\n".format(i)

    """
    bad_separator = """BEGIN PROGRAM
END PROGRAM"""

    input_ = input_.replace(bad_separator, '')

    program_pattern = re.compile("BEGIN PROGRAM((?!BEGIN PROGRAM).)*END PROGRAM", re.DOTALL)
    programs = program_pattern.finditer(input_)

    for program in programs:

        separator = program.group()

        to_subprocess = program.group()\
                               .replace("BEGIN PROGRAM", '')\
                               .replace("END PROGRAM", '')

        ns = {}
        exec(to_subprocess, ns)
        if 'xxx' in ns.keys():
            result = ns['xxx']

        else:
            result = ""
        # print(ns['xxx'])
        input_ = input_.split(separator)
        input_ = input_[0] + result + input_[1]

    while '\n\n\n' in input_:
        input_ = input_.replace('\n\n\n', '\n\n')

    out = input_

    return out


