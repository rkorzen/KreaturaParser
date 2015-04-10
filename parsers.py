import re
import subprocess
from elements import Block, Page, Question, Cafeteria

def block_parser(line):
    """
    :param line: String
    :rtype: Block


    """

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
    """
    :param line: String
    :rtype: Page

    """
    id = line.split(' ', 2)[1]
    page = Page(id)

    if " --hide:" in line:
        page.hide = line.split(" --hide:")[1]

    return page


def question_parser(line):
    """
    :param line: String
    :rtype: Question

    """
                    #  1                            2                   3           4                     5
    r = re.compile("^Q (S|M|L|N|O|LHS|SDG|T|B|G){1}([0-9]+_[0-9]+){0,1} ([\w_.]+){1}( --p:([\w_.]+)){0,1} (.*)$").match(line)
    question = Question(r.group(3))  # id
    question.typ = r.group(1)

    if r.group(2):                   # size opena
        size = r.group(2).split('_')
        question.size = size

    if r.group(5):
       question.parent_id = r.group(5)

    question.content = r.group(6)    # content

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


def cafeteria_parser(line):
    """
    :param line: String
    :rtype: Cafeteria

    """
    cafeteria = Cafeteria()
    cafeteria_pattern = re.compile("^((\d+)(\.d|\.c)? )?([\w&\\\\ /]+)( --hide:([\w\d ='\":\{\}\$#]+))?( --out)?$")
    # cafeteria_pattern = re.compile("^((\d+)(\.d|\.c)? )?([\w& /"+r"\\"+"]+)( --hide:([\w\d ='\":\{\}\$#]+))?( --out)?$") # to samo tylko nieco inaczej

    caf = cafeteria_pattern.match(line)

    if caf.group(2):
        cafeteria.id = caf.group(2)

    if caf.group(4):
        cafeteria.content = caf.group(4)

    if caf.group(3) == ".d":
        cafeteria.deactivate = True

    if caf.group(3) == ".c":
        cafeteria.other = True

    if caf.group(6):
        cafeteria.hide = caf.group(6)

    if caf.group(7):
        cafeteria.out = True

    return cafeteria


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

    #program_pattern = re.compile("((BEGIN PROGRAM)(\\n[\\n\w\d\"\[\]\():,\{}+=\. ']*)(END PROGRAM))", re.DOTALL)
    program_pattern = re.compile("BEGIN PROGRAM((?!BEGIN PROGRAM).)*END PROGRAM", re.DOTALL)

    # programs = program_pattern.findall(input_)
    # print(programs)
    matches = [m.groups() for m in program_pattern.finditer(input_)]

    out = ""

    programs = program_pattern.finditer(input_)

    bad_separator = """BEGIN PROGRAM
END PROGRAM"""
    print(type(bad_separator))

    for program in programs:
        separator = program.group()
        print(type(separator))

        if separator is not bad_separator:
            print(separator)

            to_subprocess = program.group().replace("BEGIN PROGRAM", '')\
                                        .replace("END PROGRAM", '')

            result = subprocess.check_output(["python", '-c', to_subprocess])
            result = str(result)[:-1].replace("b'", '')\
                                     .replace(r"\r\n", '\n')

            input_ = input_.split(separator)
            print(input_)
            input_ = input_[0] + result + input_[1]




    # for match in matches:
    #     if match[1] == "BEGIN PROGRAM":
    #         #print(match)
    #         out = subprocess.check_output(["python", '-c', match[2]])
    #         out = str(out)[:-1].replace("b'", '')\
    #                            .replace(r"\r\n", '\n')
    #
    #         wyrazenie = match[1]+match[2]+match[3]
    #         #print("wyrazenie = " + wyrazenie)
    #         in_ = input_.split(wyrazenie)
    #         input_ = in_[0] + out + in_[1]


    input_ = input_.replace("BEGIN PROGRAM", '')\
                   .replace("END PROGRAM", '')

    while '\n\n' in input_:
        input_ = input_.replace('\n\n', '\n')

    out = input_
    #print(out+"\n\n\n")
    return out




# input_ = """B B0
# BEGIN PROGRAM
# for i in range(2):
#     print('P P{0}'.format(i))
#
# END PROGRAM
#
# B B1
# BEGIN PROGRAM
# for i in range(2):
#     print('P Q{0}'.format(i))
#
# END PROGRAM
# """
#
# program_parser(input_)