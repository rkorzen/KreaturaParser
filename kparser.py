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

    if line == "_" or line == "_\n" or re.compile("^[_]+$").match(line):
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

    cafeteria_pattern = re.compile("^((\d+)(\.d|\.c)? )?([\w &\\\\/]+)( --hide:([/\:#\$\[\]\w\d\{\} \";' =]+))"
                                   "?( --out)?$")
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


def print_tree(lista):
    deep = 0
    for blok in lista:
        print(blok.id)
        print(len(blok.childs))

        for child in blok.childs:

            deep = 1
            print("\t"*deep + child.id)


def parse(text_input):
    """
    :param text_input: String
    :rtype : String (xml)


    Główny parser.

    Parser ma zadania:
        1. rozpoznać struktury
        2. zapisać je do słownika struktur
        3. zapisuje relacje pomiedzy strukturami

    Struktury to: bloki, strony, pytania


    """

    survey_blocks = []

    # ustawienia początkowe
    current_element = None
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
                current_block.childs.append(b)
            else:
                current_block = b
                survey_blocks.append(current_block)

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

            if not current_block:
                current_block = block_parser("B Default")
                survey_blocks.append(current_block)

            current_block.childs.append(current_page)
            current_element = current_page

        # endregion

        # region question
        if structure == "QUESTION":
            # region reset
            collect_statements = False
            # endregion

            current_question = question_parser(line)

            if not current_block:
                current_block = block_parser("B Default")
                survey_blocks.append(current_block)

            if not current_page:
                tmp_line = "P " + current_question.id + "_p"
                current_page = page_parser(tmp_line)
                current_block.childs.append(current_page)

            current_page.childs.append(current_question)

        # endregion

        # region cafeteria
        if structure == "CAFETERIA":
            statement = cafeteria_parser(line)

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
            current_element.precode = line.split('PRE ')[1]
        # endregion

        # region postcode
        if structure == "POSTCODE":
            current_element.postcode = line.split('POST ')[1]
        # endregion

        # region postcode
        if structure == "BLANK":
            collect_statements = False
            current_page = None
        # endregion
    return survey_blocks

if __name__ == "__main__":
    input_text = """B WSTEP
Q S L Q Proszę wybrać język ankiety / Choose language version of the questionnaire.
Polski
English

Q L INTRO Informacja o badaniu	Information about the study

Q S Q0 Proszę zaznaczyć swoją płeć (Ta informacja jest konieczna, aby treść ankiety wyświetlała się w odpowiedniej formie)
0 Kobieta
1 Mężczyzna

Q SLIDER Q1 Proszę zaznaczyć na ile zgadza się Pan(i) z każdym z poniższych stwierdzeń. Może Pan(i) umieścić suwak w dowolnym punkcie na skali od 0 od _
_
1 Czuję, że w NIVEA Polska stanowię część zespołu
2 Czuję silne, osobiste przywiązanie do NIVEA Polska
3 Jestem dumny(a) z tego, że pracuję w NIVEA Polska
4 NIVEA Polska zasługuje na moją lojalność

Q T Q2 a
0 0 bardzo NIEzadowolony(a)
1 1
2 2
3 3
4 4
5 5 ani zadowolony(a) ani niezadowolony(a)
6 6
7 7
8 8
9 9
10 10 bardzo zadowolony(a)
_
Biorąc pod uwagę Pana(i) własne doświadczenia, na ile jest Pan(i) zadowolony(a) z pracy w NIVEA Polska?

Q S Q3 Proszę zaznaczyć, w jakim stopniu zgadza się Pan(i) z każdym z poniższych stwierdzeń. Może Pan(i) umieścić suwak w dowolnym punkcie na skali od 0 od 10, gdzie „0” oznacza – „zdecydowanie NIE”, a „10” – „zdecydowanie TAK”. Pozostałe liczby od 1 do 9 służą do wyrażenia opinii pośrednich.
NIVEA Polska jest jedną z najlepszych marek w branży
Podobają mi się wartości mojej firmy
Podobają mi się wartości marki NIVEA
Polecam produkty i usługi, które produkuje moja firma
Moja firma wykazuje dbałość o sprawy społeczne i uczestniczy w akcjach charytatywnych
Ogólnie rzecz biorąc, moja firma jest godna zaufania
Jestem przekonany(a), że moja firma sprosta przyszłym wyzwaniom w branży
Moja firma jest nowoczesna, ma dużo nowych pomysłów i idei
Moja firma oferuje jedne z najbardziej innowacyjnych produktów na polskim rynku lub Moja firma oferuje innowacyjne kosmetyki, które powstały w oparciu o najnowsze badania
_
0 0 zdecydowanie NIE
1 1
2 2
3 3
4 4
5 5 ani TAK ani NIE
6 6
7 7
8 8
9 9
10 10 zdecydowanie TAK

Q S Q4 Czy w ciągu ostatnich 12 miesięcy Pana(i) opinia na temat Pana(i) firmy...?
1 zdecydowanie się poprawiła
2 raczej się poprawiła
3 nie zmieniła się
4 raczej się pogorszyła
5 zdecydowanie się pogorszyła

1.	Historia firmy NIVEA na świecie
2.	Historia firmy NIVEA w Polsce
3.	Pozycja rynkowa firmy NIVEA (np. wskaźniki sprzedażowe i znajomość marki)
4.	Oferta, asortyment firmy NIVEA
5.	Działanie i właściwości poszczególnych produktów NIVEA
6.	Akcje CSR-owe prowadzone przez firmę NIVEA
7.	Komunikacja firmy NIVEA z konsumentami (reklama)
8.	Konkursy, loterie, akcje promocyjne firmy NIVEA
9.	Testy porównawcze produktów NIVEA vs konkurencja
10.	Wartości firmy NIVEA
11.	Wartości marki NIVEA

Q SDG 5. Używając poniższej skali, proszę określić, na ile ważne i przydatne są poszczególne obszary wiedzy na temat firmy NIVEA w Pana(i) codziennej pracy?
1 Bardzo ważne i przydatne
2 Dość ważne i przydatne
3 Przeciętnie ważne i przydatne
4 Nieważne i nieprzydatne
_
1 Historia firmy NIVEA na świecie SINGLE CHOICE
2 Historia firmy NIVEA w Polsce SINGLE CHOICE
3 Pozycja rynkowa firmy NIVEA (np. wskaźniki sprzedażowe i znajomość marki) SINGLE CHOICE
4 Oferta, asortyment firmy NIVEA SINGLE CHOICE
5 Działanie i właściwości poszczególnych produktów NIVEA SINGLE CHOICE
6 Akcje CSR-owe prowadzone przez firmę NIVEA SINGLE CHOICE
7 Komunikacja firmy NIVEA z konsumentami (reklama) SINGLE CHOICE
8 Konkursy, loterie, akcje promocyjne firmy NIVEA SINGLE CHOICE
9 Testy porównawcze produktów NIVEA vs konkurencja SINGLE CHOICE
10 Wartości firmy NIVEA SINGLE CHOICE
11 Wartości marki NIVEA SINGLE CHOICE

Q SDG Q6 Które ze stwierdzeń najlepiej opisuje Pana(i) wiedzę na temat firmy NIVEA w poszczególnych obszarach?
1 mam bardzo dużą wiedzę na ten temat i czuję się swobodnie w rozmowach z różnymi ludźmi (np. kontrahentami, znajomymi)
2 mam dużą wiedzę na ten temat, jednak nie zawsze jest ona wystarczająca aby swobodnie odpowiadać na pytania różnych ludzi (np. kontrahentów, znajomych)
3 mam wiedzę wystarczającą aby czuć się dość swobodnie w rozmowach z różnymi ludźmi (np. kontrahentami, znajomymi)
4 moja wiedza na ten temat jest niewystarczająca
_
1 Historia firmy NIVEA na świecie SINGLE CHOICE
2 Historia firmy NIVEA w Polsce SINGLE CHOICE
3 Pozycja rynkowa firmy NIVEA (np. wskaźniki sprzedażowe i znajomość marki) SINGLE CHOICE
4 Oferta, asortyment firmy NIVEA SINGLE CHOICE
5 Działanie i właściwości poszczególnych produktów NIVEA SINGLE CHOICE
6 Akcje CSR-owe prowadzone przez firmę NIVEA SINGLE CHOICE
7 Komunikacja firmy NIVEA z konsumentami (reklama) SINGLE CHOICE
8 Konkursy, loterie, akcje promocyjne firmy NIVEA SINGLE CHOICE
9 Testy porównawcze produktów NIVEA vs konkurencja SINGLE CHOICE
10 Wartości firmy NIVEA SINGLE CHOICE
11 Wartości marki NIVEA SINGLE CHOICE

Q M Q7 W których obszarach dotyczących firmy NIVEA chciał(a)by Pan(i) poszerzyć swoją wiedzę w pierwszej kolejności. Proszę zaznaczyć maksymalnie dwa obszary.Może też Pan(i) zaznaczyć odpowiedzi: &lt;br&gt;- „inne” - aby wskazać inne obszary, którymi jest Pan(i) zainteresowany(a) &lt;br&gt;- „żadne” - jeśli nie jest Pan(i) zainteresowany poszerzaniem wiedzy nt. firmy NIVEA.
1 Historia firmy NIVEA na świecie
2 Historia firmy NIVEA w Polsce
3 Pozycja rynkowa firmy NIVEA (np. wskaźniki sprzedażowe i znajomość marki)
4 Oferta, asortyment firmy NIVEA
5 Działanie i właściwości poszczególnych produktów NIVEA
6 Akcje CSR-owe prowadzone przez firmę NIVEA
7 Komunikacja firmy NIVEA z konsumentami (reklama)
8 Konkursy, loterie, akcje promocyjne firmy NIVEA
9 Testy porównawcze produktów NIVEA vs konkurencja
10 Wartości firmy NIVEA
11 Wartości marki NIVEA
96.c inne (jakie? ...)
97.d żadne

Q O90_4 Q7a Proszę napisać, dlaczego nie jest Pan(i) zainteresowany(a) poszerzaniem wiedzy nt. firmy NIVEA?

Q M Q8 Interesuje Pana(ią) wiedza z zakresu oferty / produktów firmy NIVEA. Proszę zaznaczyć, którymi kategoriami jest Pana(i) najbardziej zainteresowany(a)?
1 Produkty do pielęgnacji ciała: np. mleczka do ciała, balsamy
2 Kremy uniwersalne
3 Dezodoranty i antyperspiranty
4 Produkty do opalania i po opalaniu
5 Produkty do pielęgnacji twarzy: kremy, maski
6 Produkty do oczyszczenia twarzy: np. toniki, mleczka, żele
7 Produkty do mycia i kąpieli: np. żele, pianki, mleczka, olejki
8 Produkty dla mężczyzn: do golenia, po goleniu, kremy do twarzy
9 Produkty dla dzieci i niemowląt
10 Produkty do pielęgnacji i stylizacji włosów
11 Produkty do pielęgnacji ust

Q O Q9 Czy są jeszcze inne aspekty dotyczące firmy NIVEA i oferowanych przez nią produktów, o których chciał(a)by Pan(i) dowiedzieć się więcej?

B O_MNIE
Q L D1_intro Ankieta jest anonimowa, dlatego aby móc w pełni ocenić sytuację panującą w poszczególnych działach/ zespołach/ departamentach bardzo prosimy o udzielenie odpowiedzi na kilka pytań, które pomogą nam zaklasyfikować odpowiedzi, zbadać ogólne trendy oraz dokonać pełnej analizy danych.  Odpowiedzi nie będą powiązane z konkretną osoba wypełniającą ankietę – są traktowane jako ściśle poufne i anonimowe. Przy każdym pytaniu proszę wybrać tylko jedną odpowiedź. Zawsze ma Pan(i) możliwość pominąć dane pytanie

Q S D1 Do jakiej grupy wiekowej Pan(i) należy?
1 poniżej 30 lat
2 30-39 lat
3 40-49 lat
4 50 lat i więcej

Q S D2 W jakim dziale/ zespole / departamencie Pan(i) pracuje?
1
2
3 nie wiem

Q S D3 Jaki jest Pana(i) staż w NIVEA Polska?
1 poniżej roku
2 1 rok do mniej niż 2 lata
3 2 lata do mniej niż 5 lat
4 5 lat do mniej niż 10 lat
5 10 lat do mniej niż 20 lat
6 20 lat lub dłużej"""

    t = parse(input_text)
    print_tree(t)
