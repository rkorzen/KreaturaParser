"""
Author: Rafał Korzeniewski
Mail: korzeniewski@gmail.com

Main module for Kreatura Parser Project.

The main function is parse

"""
import re
from lxml import etree
from parsers import block_parser, page_parser, question_parser, cafeteria_parser, program_parser
from elements import Question, Survey
# from lxml import etree




def recognize(line):
    """text -> text

    Ma za zadanie rozpoznać co to za struktura.

    :param line:

    Strukturą mogą być:
    :BLOK: B B0
    :PAGE: P P0
    :QUSTION: Q S Q1 trsc
    :CAFETERIA: 1 element 1
    :SWITCH: _

    oraz struktury specjalne:
    :START LOOP: --BEGIN FOR
    :END LOOP: --END FOR


    Każdy element ma ID
        BLOK i PAGE: line.split(' ')[1] - na drugiej pozycji
        QUESTION: line.split(' ')[2] - na 3 pozycji

    Każdy element może mieć rodzica (opcjonalnie):
        BLOK i PAGE: line.split(' ')[1]
        QUESTION: --parent: B0

    BLOKI i STRONY mogą mieć precode

    STRONY mogą być tworzone explicite, albo domyślnie - poprzez dodanie _p do id question

    Struktury mogą mieć dodatkowe atrybuty:
    --rot
    --ran
    --hide: pattern

    """
    line = clean_line(line)  # czyszczę linię

    # example: "_"
    if line == "_" or line == "_\n" or re.compile("^[_]+$").match(line):
        return "SWITCH"

    # example: B B1 B0 --ran --hide: $A1:{0} == "1"
    block_pattern = re.compile("^(B)(( )[\w_.]+){1,2}(( --ran)|( --rot))?( --hide:.*)?$")
    if block_pattern.match(line):
        return "BLOCK"

    # example: P P0 --hide: $A1:{0} == "1"
    page_pattern = re.compile("^(P )([\w_.]+)*(([ ])*((--hide:)(.*)))*$")  # z grupowaniem
    if page_pattern.match(line):
        return "PAGE"

    # example: Q O Q1 Coś tam --rot --hide
    question_pattern = re.compile("^Q (S|M|L|N|O|LHS|SDG|T|B|G)([0-9]+_[0-9]+)? [\w_.]+ (.*)$")
    if question_pattern.match(line):
        return "QUESTION"

    precode_pattern = re.compile("^PRE .*$")
    if precode_pattern.match(line):
        return "PRECODE"

    precode_pattern = re.compile("^POST .*$")
    if precode_pattern.match(line):
        return "POSTCODE"

    comment_line_patrn = re.compile("^//.*$")
    if comment_line_patrn.match(line):
        return "COMMENT"

    caf_patrn = re.compile("^((\d+)(\.d|\.c)? )?([\w &\\\\/]+)( --hide:([/\:#\$\[\]\w\d\{\} \";' =]+))?( --so| --gn)?$")
    # if caf_patrn.match(line) and not line.startswith("B ") and not line.startswith("P "):
    if caf_patrn.match(line):
        return "CAFETERIA"

    blanck_pattern = re.compile("^$")
    if blanck_pattern.match(line):
        return "BLANK"


def clean_line(line):
    """:rtype : string

    Funkcja ma za zadanie oczyść linię ze zbędnych odstępów, tabulacji
    ? Ewentualne znaki & zamienić powinna na &amp;

    """
    line = line.replace("\t", ' ')
    line = " ".join(line.split())
    line = line.strip()
    line = line.replace('&', '&amp;')
    line = line.replace('&amp;amp;', '&amp;')

    return line


def print_tree(survey):
    """Wizualizuje drzewo elementow"""
    out = []

    def element_tree(element, level=0):
        out.append('\t'*level + element.id)
        if not element.childs:
            pass
        else:
            for child in element.childs:
                element_tree(child, level+1)

    bloki = survey.childs
    for blok in bloki:
        element_tree(blok)

    return '\n'.join(out)


def parse(text_input):
    """
    :param text_input: String
    :rtype : String (xml)


    Główny parser.

    Parser ma zadania:
        1. Sprawdza, czy w wejściu są bloki programu i jeśli tak to wykonuje je.
        2. Dzieli wejście na linie i dla każdej linii sprawdza co to jest a następnie woła odpowiedni parser
        3. Dodaje obiekty do ich rodziców. Jeśli trzeba to tworzy rodzica

    Struktury to: bloki, strony, pytania



    """

#    # TODO: Źle parsuje kafeterię - ucina elementy, gdy jest więcej niż dwa znaczniki
#    np: """Q S Q1 COS
# A --gn
# B --so"""

    survey = Survey()

    next_page_precode = [None, None]

    # ustawienia początkowe
    current_element = None
    current_block = None
    current_page = None
    current_question = None
    collect_statements = False

    # sprawdzamy czy są wewnątrz bloki programow

    text_input = program_parser(text_input)

    # dzielimy wejście na linie:
    text_input = text_input.splitlines()

    # dla każdej linii musimy sprawdzić co to jest
    for line in text_input:

        structure = recognize(line)  # rozpoznaję strukturę

        # w zależności od tego co to jest reagujemy tworząc odpowiednie obiekty

        # region block
        if structure == "BLOCK":

            # region reset
            """
                Jeśli wieresz to nowa struktura BLOCK/PAGE/QUESTION,
                to poprzednie pytane sie kończy i trzeba się znowu
                przełączyć na zbieranie kafeterii odpowiedzi a nie stwierdzeń

            """
            collect_statements = False

            """
                pojawił się blok, więc poprzednia strona powinna być pusta,
                Jeśli następny element będzie typy QUESTION, to będzie wiadomo,
                że trzeba utworzyć też PAGE
            """
            current_page = None

            # endregion

            b = block_parser(line)

            if b.parent_id:
                survey.add_to_parent(b)
            else:
                current_block = b
                survey.append(current_block)

            current_element = current_block

        # endregion

        # region page
        if structure == "PAGE":

            # region reset
            """
                Jeśli wieresz to nowa struktura BLOCK/PAGE/QUESTION,
                to poprzednie pytane sie kończy i trzeba się znowu
                przełączyć na zbieranie kafeterii odpowiedzi a nie stwierdzeń

            """

            collect_statements = False
            # endregion

            current_page = page_parser(line)
            print('AA', next_page_precode)
            if next_page_precode[0] != None:
                print('AAA')
            if current_page.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_page.precode = next_page_precode[1]
                next_page_precode = [None, None]

            if not current_block:
                current_block = block_parser("B Default")
                survey.append(current_block)

            current_block.childs.append(current_page)
            current_element = current_page

        # endregion

        # region question
        if structure == "QUESTION":
            # region reset
            collect_statements = False

            # endregion

            current_question = question_parser(line)

            try:
                """
                W current element mamy question, a nowy element to też question
                jeśli wieć nie ma on parrent_id, to trzeba utworzyć nową stronę

                """
                if not current_question.parent_id and isinstance(current_element, Question):
                    current_page = None
            except AttributeError:
                """To raczej nie wymaga testu."""
                pass

            if not current_block:
                current_block = block_parser("B Default")
                survey.append(current_block)

            if not current_page:
                tmp_line = "P " + current_question.id + "_p"
                current_page = page_parser(tmp_line)
                current_block.childs.append(current_page)

            current_page.childs.append(current_question)
            current_element = current_question

            # print('AA', next_page_precode)

            if current_page.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_page.precode = next_page_precode[1]
                next_page_precode = [None, None]

        # endregion

        # region cafeteria
        if structure == "CAFETERIA":
            print(line)
            statement = cafeteria_parser(line)
            # print('Statement', statement)
            """jeśli nie ma numeru kafeterii to nadajemy go - albo dla kafeterii odpowiedzi (cafeteria),
               albo dla kafeterii stwierdzen (statements), jeśli akurat je zbieramy.

               To jest potrzebne do wyliczania filtrow screenout i gotonext
            """
            if not statement.id:
                if not collect_statements:
                    ktory = len(current_question.cafeteria)
                    statement.id = str(ktory + 1)
                else:
                    ktory = len(current_question.statements)
                    statement.id = str(ktory + 1)

            """Do warunku bierzemy:

            id pytania (question.id)
            nr odpowiedzi

            """

            if statement.screenout:
                current_page.postcode += '''if (${0}:{1} == "1")\n  #OUT = "1"\n  goto KONKURS\nelse\nendif'''.format(
                    current_question.id, statement.id
                )
                # if current_page.postcode:
                #     current_page.postcode += '''if (${0}:{1} == "1")\n  #OUT = "1"\n  goto KONKURS\nelse\nendif'''.format(
                #         current_question.id, statement.id
                #     )
                # else:
                #     current_page.postcode = '''if (${0}:{1} == "1")\n  #OUT = "1"\n  goto KONKURS\nelse\nendif'''.format(
                #         current_question.id, statement.id
                #     )

            if statement.gotonext:
                # print("statement", statement)
                # goto next musimy dać na następnej stronie

                if next_page_precode[0] is None:
                    next_page_precode = [current_page.id, '''if (${0}:{1} == "1");  goto next;else;endif'''.format(current_question.id, statement.id)]
                else:
                    next_page_precode[1] += ''';;if (${0}:{1} == "1");  goto next;else;endif'''.format(current_question.id, statement.id)
                    # print('CC', next_page_precode)
            if collect_statements:
                current_question.statements.append(statement)
            else:
                current_question.cafeteria.append(statement)
        # endregion

        # region switch
        if structure == "SWITCH":
            collect_statements = True

        # endregion

        # region precode
        if structure == "PRECODE":
            if type(current_element) is Question:
                current_page.precode = line.split('PRE ')[1]
            else:
                current_element.precode = line.split('PRE ')[1]
        # endregion

        # region postcode
        if structure == "POSTCODE":
            if type(current_element) is Question:
                current_page.postcode = line.split('POST ')[1]
            else:
                current_element.postcode = line.split('POST ')[1]
        # endregion

        # region postcode
        if structure == "BLANK":
            collect_statements = False
            # current_page = None
        # endregion

    return survey

input_ = """Q S Q1 COS
A --so
B --so"""

parse(input_)
#
# text = '''B B0
# Q S Q1 A
# 1 a
# 2 b
#
# Q S Q2 B
# 1 a --hide:$Q1{0} == "1"
# 2 b
# '''
# p = parse(input_)
# p.to_xml()
#
# with open('test.xml', 'wb') as f:
#     f.write(etree.tostring(p.xml, pretty_print=True))