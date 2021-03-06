# coding: utf-8
import re
from sdl.parsers import block_parser, page_parser, question_parser, cafeteria_parser, program_parser, Patterns
from sdl.elements import Question, Survey, Page, Block
from sdl.tools import find_parent, clean_line, find_by_id

"""
Author: Rafał Korzeniewski
Mail: korzeniewski@gmail.com

Main module for Kreatura Parser Project.

The main function is parse

"""


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
    # block_pattern = re.compile("^(B)(( )[\w_.]+){1,2}(( --ran)|( --rot))?( --hide:.*)?$")
    block_pattern = Patterns.block_pattern
    if block_pattern.match(line):
        return "BLOCK"

    # example: P P0 --hide: $A1:{0} == "1"
    # page_pattern = re.compile("^(P )([\w_.]+)*(([ ])*((--hide:)(.*)))*$")  # z grupowaniem
    page_pattern = Patterns.page_pattern
    if page_pattern.match(line):
        return "PAGE"

    # example: Q O Q1 Coś tam --rot --hide
    # question_pattern = re.compile("^Q (S|M|L|N|O|LHS|B|SDG|T|G|SLIDER)([0-9]+_[0-9]+)? [\w_.]+ (.*)$")
    question_pattern = Patterns.question_pattern
    if question_pattern.match(line):
        return "QUESTION"

    # precode_pattern = re.compile("^PRE .*$")
    precode_pattern = Patterns.precode_pattern
    if precode_pattern.match(line):
        return "PRECODE"

    # postcode_pattern = re.compile("^POST .*$")
    postcode_pattern = Patterns.postcode_pattern
    if postcode_pattern.match(line):
        return "POSTCODE"

    # comment_line_patrn = re.compile("^//.*$")
    comment_line_pattern = Patterns.comment_line_pattern
    if comment_line_pattern.match(line):
        return "COMMENT"

    loop_pattern = Patterns.loop_pattern
    if loop_pattern.match(line):
        return "LOOP"

    caf_pattern = Patterns.caf_pattern
    if caf_pattern.match(line):
        return "CAFETERIA"

    blanck_pattern = Patterns.blanck_pattern
    if blanck_pattern.match(line):
        return "BLANK"

    print("Nie wiem co to jest", line)
    return "Struktura nie rozpoznana", line

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
    tmp_questions_id = []
    survey = Survey()

    next_page_precode = [None, None]

    # ustawienia początkowe
    current_element = None
    current_block = None
    current_page = None
    current_question = None
    collect_statements = False
    collect_categories = False
    add_id_to_content = False
    reorder_statements = False
    # sprawdzamy czy są wewnątrz bloki programow

    text_input = program_parser(text_input)

    # dzielimy wejście na linie:
    text_input = text_input.splitlines()

    # dla każdej linii musimy sprawdzić co to jest
    for line in text_input:
        if line.startswith('\\'):
            continue

        line = line.strip()  # usuwam nadmiarowe spacje itp
        structure = recognize(line)  # rozpoznaję strukturę

        if structure in ["BLOCK", "QUESTION", "SWITCH", "LOOP", "PRECODE", "POSTCODE"]:
            add_id_to_content = False
            rename_statements = False

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
            collect_categories = False
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
                current_block = b

            else:
                current_block = b
                survey.append(current_block)

            current_element = current_block

        # endregion

        # region page
        if structure == "PAGE":
            # print('BBB')
            # region reset
            """
                Jeśli wieresz to nowa struktura BLOCK/PAGE/QUESTION,
                to poprzednie pytane sie kończy i trzeba się znowu
                przełączyć na zbieranie kafeterii odpowiedzi a nie stwierdzeń

            """

            collect_statements = False
            collect_categories = False
            # endregion

            current_page = page_parser(line)

            if not current_block:
                current_block = block_parser("B Default")
                survey.append(current_block)

            if current_page.parent_id:
                block = find_by_id(survey, current_page.parent_id)
                block.childs.append(current_page)
            else:
                current_block.childs.append(current_page)

            current_element = current_page

        # endregion

        # region question
        if structure == "QUESTION":
            # region reset
            collect_statements = False
            collect_categories = False
            # endregion

            current_question = question_parser(line)
            if current_question.id in tmp_questions_id:
                raise ValueError("Two questions have the same id: " + current_question.id)
            else:
                tmp_questions_id.append(current_question.id)
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

            if current_page.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_page.precode = next_page_precode[1]
                next_page_precode = [None, None]

        # endregion

        # region cafeteria
        if structure == "CAFETERIA":
            try:
                statement, add_id_to_content = cafeteria_parser(line, add_id_to_content)
            except AttributeError:
                raise AttributeError('Błąd w linii: ', line)

            # jeśli nie ma numeru kafeterii to nadajemy go -
            # dla kafeterii odpowiedzi (cafeteria),
            # albo dla kafeterii stwierdzen (statements), jeśli akurat je zbieramy.
            # To jest potrzebne do wyliczania filtrow screenout i gotonext

            try:
                if int(statement.id) < 0:
                    rename_statements = True

            except TypeError:
                pass


            if not statement.id or rename_statements:
                if not collect_statements:   # kafeteria odpowiedzi
                    try:
                        ktory = len(current_question.cafeteria)
                        statement.id = str(ktory + 1)
                    except AttributeError as e:
                        raise AttributeError("Błąd w linii", line)
                else:  # kafeteria stwierdzeń
                    ktory = len(current_question.statements)
                    statement.id = str(ktory + 1)


            if statement.gotonext:
                # print("statement", statement)
                # goto next musimy dać na następnej stronie

                if next_page_precode[0] is None:
                    next_page_precode = [current_page.id, '''if (${0}:{1} == "1");  goto next;else;endif'''.format(
                        current_question.id, statement.id)]
                else:
                    next_page_precode[1] += ''';;if (${0}:{1} == "1");  goto next;else;endif'''.format(
                        current_question.id, statement.id)
                    # print('CC', next_page_precode)

            if collect_statements:
                current_question.statements.append(statement)
            elif collect_categories:
                current_question.categories.append(statement)
            else:
                current_question.cafeteria.append(statement)

            if statement.goto:
                if next_page_precode[0] is None:
                    next_page_precode = [current_page.id, '''if (${0}:{1} == "1");  goto {2};else;endif'''.format(
                        current_question.id, statement.id, statement.goto)]
                else:
                    next_page_precode[1] += ''';;if (${0}:{1} == "1");  goto {2};else;endif'''.format(
                        current_question.id, statement.id, statement.goto)

        # endregion

        # region switch
        if structure == "SWITCH":
            collect_statements = True

        # endregion

        # region loop for categories
        if structure == "LOOP":
            collect_categories = True
            collect_statements = False
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

        # region BLANK
        if structure == "BLANK":
            collect_statements = False
            # current_page = None
        # endregion

        if isinstance(current_element, Page) or isinstance(current_element, Block):
            if current_element.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_element.precode = next_page_precode[1]
                next_page_precode = [None, None]

    return survey

if __name__ == "__main__":
    #with open(r'/home/korzen/workspace/mockups/x.txt', 'r') as f:
    with open(r"c:\badania\ADHOC.2016\127659.06\DIME\SKRYPT\skrypt.txt") as f:
        f = f.read()
        survey = parse(f)
        survey.to_spss()
        print(survey.spss_out)
