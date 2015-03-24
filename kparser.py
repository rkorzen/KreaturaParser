import re


class SurveyElements():
    """Base of survey structures/elements"""
    def __init__(self):
        self.precode = False
        self.postcode = False
        self.rotation = False
        self.random = False
        self.hide = False


class Block(SurveyElements):
    def __init__(self, id):
        SurveyElements.__init__(self)
        self.id = id
        self.childs = []
        self.parent_id = False

    def __eq__(self, other):
        return self.id == other.id and \
               self.parent_id == other.parent_id and \
               self.precode == other.precode and \
               self.postcode == other.postcode and \
               self.rotation == other.rotation and \
               self.random == other.random and \
               self.hide == other.hide and \
               self.childs == other.childs


class Page(SurveyElements):
    def __init__(self):
        super().__init__()
        self.questions = []


class Question(SurveyElements):
    """Question"""
    def __init__(self):
        super().__init__()
        self.typ = ""
        self.cafeteria = []
        self.statements = []


class ListElement():
    """List element - to np cafeteria, statements"""
    def __init__(self, id):
        self.id = ""
        self.content = ""
        self.hide = ""


def recognize(line):

    """text -> text

    Ma za zadanie rozpoznać co to za struktura.
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
    line = clean_line(line)         # czyszczę linię

    if line == "_" or line == "_\n":
        return "SWITCH"

    # block example: B B1 B0 --ran --hide: $A1:{0} == "1"
    block_pattern = re.compile("^(B)(( )[\w_.]+){1,2}(( --ran)|( --rot)){0,1}( --hide:.*){0,1}$")

    if block_pattern.match(line):
        return "BLOCK"

    page_pattern = re.compile("^(P )([\w_.]+)*(([ ])*((--hide:)(.*)))*$")  # z grupowaniem
    if page_pattern.match(line):
        return "PAGE"

    question_pattern = re.compile("^Q (S|M|L|N|O|LHS|SDG|T|B|G) [\w_.]+ .*$")
    if question_pattern.match(line):
        return "QUESTION"

    precode_pattern = re.compile("^PRE .*$")
    if precode_pattern.match(line):
        return "PRECODE"

    precode_pattern = re.compile("^POST .*$")
    if precode_pattern.match(line):
        return "POSTCODE"


def clean_line(line):
    """text -> text

    Funkcja ma za zadanie oczyść linię ze zbędnych odstępów, tabulacji
    ? Ewentualne znaki & zamienić powinna na &amp;

    """
    line = line.replace("\t", ' ')
    line = " ".join(line.split())
    line = line.strip()
    line = line.replace('&', '&amp;')
    line = line.replace('&amp;amp;', '&amp;')

    return line


def question_parser(line):
    pass


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

def parse(text_input):
    """
    text -> xml

    Główny parser.

    Parser ma zadania:
        1. rozpoznać struktury
        2. zapisać je do słownika struktur
        3. zapisuje relacje pomiedzy strukturami

    Struktury to: bloki, strony, pytania


    """

    # ustawienia początkowe
    current_block = None
    current_page = None
    current_question = None


    # dzielimy wejście na linie:
    text_input = text_input.splitlines()

    # dla każdej linii musimy sprawdzić co to jest
    for line in text_input:

        structure = recognize(line)     # rozpoznaję strukturę

        # w zależności od tego co to jest reagujemy tworząc odpowiednie obiekty
        if structure == "BLOCK":
            current_block = block_parser(line)

        if structure == "PAGE":
            pass

        if structure == "QUESTION":
            pass

        if structure == "SWITCH":
            pass

        if structure == "PRECODE":
            pass

        if structure == "POSTCODE":
            pass


if __name__ == "__main__":
    input = """B B0
B B1"""

    parse(input)