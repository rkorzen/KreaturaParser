# coding: utf-8
"""
Author: Rafał Korzeniewski
Mail: korzeniewski@gmail.com

Main module for Kreatura Parser Project.

The main function is parse

"""
import re
from parsers import block_parser, page_parser, question_parser, cafeteria_parser, program_parser, Patterns
from elements import Question, Survey, Page, Block
from lxml import etree
from tools import find_parent
from bs4 import BeautifulSoup



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

    # caf_patrn = re.compile("^((\d+)(\.d|\.c)? )?([\w &\\\\/]+)( --hide:([/:#\$\[\]\w\d\{\} \";'=]+))?( --so| --gn)?$")
    # caf_patrn = re.compile("[\w !@#$%^&*()_+-=.,'\":;\\|\[\]\{\}`]+")
    # caf_patrn = re.compile("^((\d+)(\.d|\.c)? )?([\w !@#$%^&*()_+-=.,'\":;\\\\|\[\]\{\}`]+)( --hide:([/:#\$\[\]\w\d\{\} \";'=]+))?( --so| --gn)?$")
    # if caf_patrn.match(line) and not line.startswith("B ") and not line.startswith("P "):
    caf_pattern = Patterns.caf_pattern
    if caf_pattern.match(line):
        return "CAFETERIA"

    blanck_pattern = Patterns.blanck_pattern
    if blanck_pattern.match(line):
        return "BLANK"

    print("Nie wiem co to jest", line)


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
                current_block = b

            else:
                current_block = b
                survey.append(current_block)

            current_element = current_block

        # endregion

        # region page
        if structure == "PAGE":
            print('BBB')
            # region reset
            """
                Jeśli wieresz to nowa struktura BLOCK/PAGE/QUESTION,
                to poprzednie pytane sie kończy i trzeba się znowu
                przełączyć na zbieranie kafeterii odpowiedzi a nie stwierdzeń

            """

            collect_statements = False
            # endregion

            current_page = page_parser(line)
            # print('AAA')
            # print(current_page.parent_id)
            # print('AA', next_page_precode)
            # if next_page_precode[0] is not None:
            #     print('AAA')

            # if current_page.id != next_page_precode[0] and next_page_precode[0] is not None:
            #     current_page.precode = next_page_precode[1]
            #     next_page_precode = [None, None]

            if not current_block:
                current_block = block_parser("B Default")
                survey.append(current_block)

            if current_page.parent_id:
                block = find_parent(survey.childs, current_page.parent_id)
                # print('BLOCK', block.id)
                block.childs.append(current_page)
            else:
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
                # print('AAA', current_page)
                tmp_line = "P " + current_question.id + "_p"
                current_page = page_parser(tmp_line)
                current_block.childs.append(current_page)

            # print(current_page.id)
            current_page.childs.append(current_question)
            current_element = current_question

            # print('AA', next_page_precode)

            if current_page.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_page.precode = next_page_precode[1]
                next_page_precode = [None, None]

        # endregion

        # region cafeteria
        if structure == "CAFETERIA":
            # print(line)
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
            else:
                # print(current_question.cafeteria)
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

        if isinstance(current_element, Page) or isinstance(current_element, Block):
            if current_element.id != next_page_precode[0] and next_page_precode[0] is not None:
                current_element.precode = next_page_precode[1]
                next_page_precode = [None, None]

    return survey


if __name__ == "__main__":
    input_ = '''B SCREENER
Q S S0 Czy pracuje Pan(i) w którejś z poniższych branż?
1 Służba zdrowia, ochrona zdrowia --so
2 Farmacja, apteki --so
3 Marketing, reklama --so
4 Badania rynku --so
5 W żadnej z powyższych

Q S S1 Czy zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy witaminy, minerały lub preparaty witaminowo-minerałowe / multiwitaminy?
1 Tak
2 Nie --so

Q M S2 Proszę wskazać, które z poniższych kategorii preparatów zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy:
1 Preparaty witaminowo-minerałowe lub multiwitaminy (np. Centrum, Vita-miner itp.)
2 Pojedyncze witaminy
3 Pojedyncze minerały
4 Witaminy lub minerały z dodatkiem
5 Inne suplementy
98.d Żadne z powyższych --so

Q M S2a Proszę wskazać, jakie witaminy zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy --ran
PRE if($S2:2 == "1");else;goto next;endif
Witamina A
Witamina B
Witamina C
Witamina D
Witamina E
Witamina K
97 Inne pojedyncze witaminy

Q M S2b Proszę wskazać, jakie minerały zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy --ran
PRE if($S2:3 == "1");else;goto next;endif
Wapń
Cynk
Potas
Magnez
Żelazo
Sód
97 Inne pojedyncze minerały

Q M S2c Proszę wskazać, jakie witaminy lub minerały z dodatkiem zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy --ran
PRE if($S2:4 == "1");else;goto next;endif
Magnez + wit.B6
Rutyna + wit.C
Omega3 + wit.E
Witamina A + E
Wapno + wit.C
97.c Inne - jakie?

Q M S2d Proszę wskazać, jakie inne suplementy zażywał(a) Pan(i) w ciągu ostatnich 3 miesięcy --ran
PRE if($S2:5 == "1");else;goto next;endif
Koenzym Q10
Kwasy omega-3
Kwasy DHA
Tran
Kolagen
97.c Inne - jakie?

Q O S3 Ile osób (łącznie z Panem/Panią) liczy Pana(i) gospodarstwo domowe?

Q S S4 Czy posiada Pan(i) dzieci w wieku poniżej 18 lat?
1 Tak
2 Nie --goto:S7_p

Q O S5 Ile dzieci poniżej 18 lat Pan(i) posiada?

Q O S6 W jakim  wieku są Pana(i) dzieci?
1 1 dziecko
2 2 dziecko
3 3 dziecko
4 4 dziecko
5 5 dziecko

Q S S7 Czy jest Pani obecnie w ciąży?
PRE if (#PLEC == "k");else;goto next;endif
1 Tak
2 Nie
3 Nie wiem / trudno powiedzieć / odmowa

B A
Q L A1_intro Mianem witamin i minerałów określa się bardzo różne preparaty, zarówno pojedyncze witaminy i minerały jak i środki złożone z wielu elementów. Teraz chcielibyśmy poznać Pana(i) zwyczaje i opinie dotyczące stosowania tego typu preparatów.

Q SDG A1 Proszę wskazać jak często zażywa Pan(i)...?
1 Codziennie
2 3-4 razy w tygodniu
3 1-2 razy w tygodniu
4 2-3 razy w miesiącu
5 Raz na miesiąc
6 Rzadziej niż raz na miesiąc
7 Nieregularnie, tylko w okresach zwiększonego zapotrzebowania / choroby
8 Nie wiem / trudno powiedzieć
_
1 Preparaty witaminowo-minerałowe lub multiwitaminy (np. Centrum, Vita-miner itp.)
2 Pojedyncze witaminy
3 Pojedyncze minerały
4 Witaminy lub minerały z dodatkiem
5 Inne suplementy'''

    input_ = '''Q SDG A1 Proszę wskazać jak często zażywa Pan(i)...?
1 Codziennie
2 3-4 razy w tygodniu
3 1-2 razy w tygodniu
4 2-3 razy w miesiącu
5 Raz na miesiąc
6 Rzadziej niż raz na miesiąc
7 Nieregularnie, tylko w okresach zwiększonego zapotrzebowania / choroby
8 Nie wiem / trudno powiedzieć
_
1 Preparaty witaminowo-minerałowe lub multiwitaminy (np. Centrum, Vita-miner itp.)
2 Pojedyncze witaminy
3 Pojedyncze minerały
4 Witaminy lub minerały z dodatkiem
5 Inne suplementy'''

    input_ = """Q G A15 Teraz wyświetlą się Panu(i) różne opinie o wybranych preparatach witaminowo-minerałowych. Który lub które z poniższych preparatów…:
1 Centrum --hide:$A14_{0}:2 == "0" && $A14_{0}:3 == "0" && $A14_{0}:4 == "0"
2 Vitaral
3 Plusssz
4 Vita-miner
5 Multi Code
6 VigorUp!
7 Olimp Labs
8 Bodymax
9 Doppelherz
10 Pharmaton Geriavit
11 Vitotal
12 Falvit
13 Vitrum Calcium
14 Vibovit
15 VisolVit
16 Marsjanki
17 Gumiżelki Witaminiaki
18 Ceruvit Junior
98 Żadne z powyższych
_
1 Jest godny zaufania
2 Jest skuteczny
3 Ma atrakcyjną cenę
4 To najlepszy preparat witaminowo-minerałowy
5 Jest modny, na czasie
6 Jest nowoczesny
7 Jest bezpieczny
8 Jest najbardziej popularny
9 To preparat dla kogoś takiego jak ja
10 To preparat, który polecił(a)bym swoim znajomym
11 Jest wysokiej jakości
12 Jest wygodny w stosowaniu
13 Jest go dużo w opakowaniu w rozsądnej cenie
14 Jest dobrze przyswajalny
15 Można go stosować w różnych formach
16 Pochodzi z naturalnych składników
17 Ładnie pachnie
18 Jest smaczny
19 Jest „chemiczny”
20 Szybko działa
21 Można go wszędzie kupić
22 Ma szeroki / bogaty skład
"""

    with open(r'c:\badania\ADHOC.2015\124747.07\IBIS\skrypt\pepperoni.txt', 'rU') as in_:

        survey = parse(in_.read())

        survey.to_xml()
        x = etree.tostring(survey.xml, pretty_print=True)
        with open(r'C:\users\korzeniewskir\Desktop\xxx.xml', 'wb') as f:
            f.write(x)

    # survey = parse(input_)
    # survey.to_xml()
    # x = etree.tostring(survey.xml, pretty_print=True)
    # with open(r'C:\users\korzeniewskir\Desktop\xxx.xml', 'wb') as f:
    #     f.write(x)

    #print(BeautifulSoup(x).prettify(formatter="xml"))


