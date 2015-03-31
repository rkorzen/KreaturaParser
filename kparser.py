import re
from parsers import block_parser, page_parser, question_parser, cafeteria_parser

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

    if line == "_" or line == "_\n":
        return "SWITCH"

    # block example: B B1 B0 --ran --hide: $A1:{0} == "1"
    block_pattern = re.compile("^(B)(( )[\w_.]+){1,2}(( --ran)|( --rot))?( --hide:.*)?$")
    if block_pattern.match(line):
        return "BLOCK"

    page_pattern = re.compile("^(P )([\w_.]+)*(([ ])*((--hide:)(.*)))*$")  # z grupowaniem
    if page_pattern.match(line):
        return "PAGE"

    question_pattern = re.compile("^Q (S|M|L|N|O|LHS|SDG|T|B|G)([0-9]+_[0-9]+)? [\w_.]+ (.*)$")
    if question_pattern.match(line):
        return "QUESTION"

    precode_pattern = re.compile("^PRE .*$")
    if precode_pattern.match(line):
        return "PRECODE"

    precode_pattern = re.compile("^POST .*$")
    if precode_pattern.match(line):
        return "POSTCODE"

    cafeteria_pattern = re.compile("^((\d+)(\.d|\.c)? )?([\w &\\\\/]+)( --hide:([/\\:#\$\[\]\w\d\{\} \";' =]+))?( --out)?$")
    if cafeteria_pattern.match(line) and not line.startswith("B ") and not line.startswith("P "):
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

def parse(text_input):
    """
    :ivar: text_input
    :rtype : sstring(xml)


    Główny parser.

    Parser ma zadania:
        1. rozpoznać struktury
        2. zapisać je do słownika struktur
        3. zapisuje relacje pomiedzy strukturami

    Struktury to: bloki, strony, pytania


    """

    survey_blocks = []

    # ustawienia początkowe
    current_block = None
    current_page = None
    current_question = None
    collect_statements = False

    # dzielimy wejście na linie:
    text_input = text_input.splitlines()

    # dla każdej linii musimy sprawdzić co to jest
    for line in text_input:

        structure = recognize(line)  # rozpoznaję strukturę

        # w zależności od tego co to jest reagujemy tworząc odpowiednie obiekty

        if structure == "BLOCK":
            current_page = None    # pojawił się blok, więc poprzednia strona powinna być pusta, tak by nic do niej nie dodać

            b = block_parser(line)
            if b.parent_id:
                current_block.childs.append(b)
            else:
                current_block = b
                survey_blocks.append(current_block)
            collect_statements = False

        if structure == "PAGE":
            current_page = page_parser(line)
            current_block.childs.append(current_page)
            collect_statements = False

        if structure == "QUESTION":

            current_question = question_parser(line)

            if not current_page:
                tmp_line = "P " + current_question.id + "_p"
                current_page = page_parser(tmp_line)

            current_page.childs.append(current_question)
            collect_statements = False

        if structure == "CAFETERIA":
            statement = statement_parser(line)

            if collect_statements:
                current_question.statements.append(statement)
            else:
                current_question.cafeteria.append(statement)

        if structure == "SWITCH":
            collect_statements = True

        if structure == "PRECODE":
            pass

        if structure == "POSTCODE":
            pass

        if structure == "BLANK":
            collect_statements = False

    return survey_blocks


if __name__ == "__main__":
    input_text = """B0"""

    t = parse(input_text)

