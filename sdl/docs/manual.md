| Title    | Survey Parser                            |
|----------|------------------------------------------|
| Subtitle | Parser mini języka ankiet                |
| Author   | Rafał Korzeniewski                       |
| email    | korzeniewski@gmail.com                   |
| web      | http://rkorzen.pythonanywhere.com/parser |
| Date:    | June 24, 2016                        | 
| Version  | 1.06                                     |


# Change Log

| Data       | Version | Description                                       | Author             |
|------------|---------|---------------------------------------------------|--------------------|
| 18.09.2015 | 1.00    | Publikacja dokumentu                              | Rafał Korzeniewski |
| 21.09.2015 | 1.01    | Spore zmiany formy, układu. Drobne zmiany treści, | Rafał Korzeniewski |
| 22.09.2015 | 1.02    | Przyklady dla Dimensions                          | Rafał Korzeniewski |     
| 05.10.2015 | 1.03    | PYTHON RECIPES                                    | Rafał Korzeniewski |
| 26.11.2015 | 1.04    | Precode/postcode - dimstyle                       | Rafał Korzeniewski |
| 26.11.2015 | 1.05    | FOR CATEGORIES - to_dim                           | Rafał Korzeniewski |
| 24.06.2016 | 1.06    | IBM BASE Professional                             | Rafał Korzeniewski |


Survey Parser
-------------

# INDEX
<!-- MarkdownTOC autolink=true autoanchor=true bracket=round depth=5 -->

- [Wstęp](#wstęp)
- [IBIS](#ibis)
  - [First things first](#first-things-first)
  - [Główne założenia](#główne-założenia)
- [Mini język ankiet](#mini-język-ankiet)
  - [Bloki](#bloki)
    - [Najprostsze wywołanie.](#najprostsze-wywołanie)
    - [Rotacja-Randomizacja](#rotacja-randomizacja)
    - [Zagnieżdzanie](#zagnieżdzanie)
    - [precode postocde](#precode-postocde)
    - [Prosta kontrola ifów w precode/postcode](#prosta-kontrola-ifów-w-precodepostcode)
  - [Page](#page)
    - [Zagnieżdzanie](#zagnieżdzanie-1)
  - [Questions](#questions)
    - [Kilka pytań na stronie](#kilka-pytań-na-stronie)
  - [Single/Multi - co można w nich zautomatyzować?](#singlemulti---co-można-w-nich-zautomatyzować)
  - [Dodatkowe skróty w Single/Multi?](#dodatkowe-skróty-w-singlemulti)
  - [Multi - minchoose/maxchoose](#multi---minchoosemaxchoose)
- [Python](#python)
  - [First blood](#first-blood)
  - [Python - zmienne](#python---zmienne)
  - [Python - string.format()](#python---stringformat)
  - [Python - listy i słowniki](#python---listy-i-słowniki)
  - [Python - pętle](#python---pętle)
  - [Funkcje i klasy](#funkcje-i-klasy)
    - [Funkcje](#funkcje)
    - [Klasy](#klasy)
- [Mini język cd...](#mini-język-cd)
  - [klauzula BEGIN PROGRAM / END PROGRAM](#klauzula-begin-program--end-program)
  - [Kontrolka Open](#kontrolka-open)
  - [Numeric](#numeric)
  - [Tabelka JS](#tabelka-js)
  - [Slider](#slider)
  - [Sliders](#sliders)
  - [Gridy](#gridy)
  - [Koszyczki](#koszyczki)
  - [Highlighter](#highlighter)
  - [Ranking](#ranking)
  - [ConceptSelect](#conceptselect)
  - [ConceptSelect z niestandardowym IbisDisablerem](#conceptselect-z-niestandardowym-ibisdisablerem)
- [Dimensions](#dimensions)
  - [Lewa strona](#lewa-strona)
    - [Podstawy](#podstawy)
    - [FOR CATEGORIES](#for-categories)
  - [Prawa strona](#prawa-strona)
  - [precod i postcode](#precod-i-postcode)
- [PYTHON RECIPES](#python-recipes)
  - [json to dict example](#json-to-dict-example)
- [English](#english)
- [Base Concepts](#base-concepts)
  - [Why WebApp?](#why-webapp)
- [Case study.](#case-study)
- [Rules:](#rules)
- [IBM Base Proffesional examples](#ibm-base-proffesional-examples)
  - [Basic question types and definitions](#basic-question-types-and-definitions)
    - [Info page](#info-page)
    - [Open question](#open-question)
    - [Numeric question](#numeric-question)
    - [Simple list definition](#simple-list-definition)
    - [Categorical single answer](#categorical-single-answer)
    - [Categorical multiple answer](#categorical-multiple-answer)
    - [Categorical with defined list](#categorical-with-defined-list)
    - [Categorical create list](#categorical-create-list)
    - [Automate cafeteria id](#automate-cafeteria-id)
      - [Examples](#examples)
        - [Basic usage:](#basic-usage)
        - [do it alphabetically - with big letters](#do-it-alphabetically---with-big-letters)
        - [`--raw-id`](#--raw-id)
        - [`--first-id`](#--first-id)
        - [Easy add bold and italic](#easy-add-bold-and-italic)
        - [REF NA DK](#ref-na-dk)
        - [cafeteria with images](#cafeteria-with-images)
      - [Sorting](#sorting)
      - [Randomize/Rotation](#randomizerotation)
  - [Another question examples](#another-question-examples)
    - [Drag and Drop](#drag-and-drop)
      - [Buckets with text](#buckets-with-text)
      - [Buckets with images](#buckets-with-images)
      - [Exclude in buckets](#exclude-in-buckets)
      - [Love hate scale with text buttons](#love-hate-scale-with-text-buttons)
      - [Love hate scale with image buttons](#love-hate-scale-with-image-buttons)
      - [Dynamic Grid](#dynamic-grid)
      - [Slider (Not implemented yet)](#slider-not-implemented-yet)
      - [Click and Fly (Not implemented yet)](#click-and-fly-not-implemented-yet)
      - [Clicakble Images](#clicakble-images)
      - [Clickable Tiles (Not implemented yet)](#clickable-tiles-not-implemented-yet)
      - [Button Matrix (Not implemented yet)](#button-matrix-not-implemented-yet)
      - [Semantic Differential (Bi-polar) - Not implemented yet](#semantic-differential-bi-polar---not-implemented-yet)
- [errors and validation](#errors-and-validation)
  - [two questions with the same id](#two-questions-with-the-same-id)
  - [two positions in cafetera have the same id](#two-positions-in-cafetera-have-the-same-id)

<!-- /MarkdownTOC -->

<a name="wstęp"></a>
# Wstęp

Automatyzacja. 

Niesie ze sobą wiele zalet. Pomaga pisać szybciej, szczególnie te bardziej założone struktury, ogranicza ilość błędów, pozwala tworzyć bardziej  czytelny i uporządkowany kod. Dzięki niej dość łatwo też nanosić poprawki. No i umówmy się - uwalnia ona nas od wielu nudnych procesów.

Nie powinna ona zwalniać jednak z myślenia. Czasem odrobina zastanowienia się pozwala stworzyć kod nie tylko w sposób zautomatyzowany, ale i wydajny z punktu widzenia serwera, czy rozsądny, dobrze uporządkowany i wygodny z punktu widzenia analizy danych.

Automatyzujcie więc procesy nudne, oczywiste, ale szukacie najlepszych dróg realizacji zadań.

Narzędzie, z którym teraz się zapoznacie może Wam w tym pomóc.

Projekt powstał jako rozwinięcie minijęzyka obsługiwanego przez narzędzie Kreatura (kreator ankiet do IBISa). Dodano nowe typy pytań, dodatkowe markery pozwalające na dodatkowe ustawienia, zagnieżdzenia, rotacje, wersjonowanie płci itd.

Obecnie (09.2015) prowadzone są prace nad użyciem tego samego wejścia do tworzenia ankiet w Dimensions. Mini język tłumaczony jest na metadata oraz routing.

<a name="ibis"></a>
# IBIS
<a name="first-things-first"></a>
## First things first
 
Kreatura - narzędzie, które pozwala na tworzenie dokumentu xml reprezentującego skrypt, a następnie wysłanie skryptu, 
oraz innych plików na serwery IBISa.

Skryp można "wyklikać" przy użyciu interfejsu samej Kreatury, jest to jednak na ogół bardzo nieefektywne, szczególnie w przypadku większych dokumentów.
Sama Kreatura dostarcza efektywniejsze rozwiązanie - parser prostego skryptu. Czyli odpowiednio sformatowane wejście:

```
B B1
P Q1_p
Q S Q1 COS
1 odp 1
2 odp 2
```

W miarę powstawania nowych rodzajów kontrolek parser ten stał się jednak coraz mniej użyteczny. Nie uwzględniał nowych typów pytań. Nie wykorzystywał też innych możliwości automatyzacji. W związku z tym, że nie był rozwijany postanowiłem napisać własny.
Pierwsza wersja nowego parsera znacznie przyspieszała prace, jednak nadal miała sporo wad. Doszedłem więc do wniosku, bogatszy o te doświadczenia, że najlepiej będzie stworzyć bardziej funkcjonalną wersję, oparta na nowych mechanizmach i pozwalającą na znacznie wygodniejszą rozbudowę, oraz wiele nowych funkcjonalności.

<a name="główne-założenia"></a>
## Główne założenia

Zgodność wsteczna - czyli zapewnienie reużywalności starych skryptów prostego języka
Jak najdalej posunięta automatyzacja
* Obsługa jak największej ilości typów kontrolek/rodzajów pytań
* Zagnieżdżanie elementów - czyli kontrola nad strukturą już na etapie skryptu PJ
* Ustawienia precode/postocde, hide, a także atrybutów bloków, stron, kontrolek - np rotacja, random, maxchoice, itd.
  (odpuściłem tutaj sobie ustawianie stylów - style powinny być ustawiane tam gdzie jest na to miejsce, czyli w arkuszu stylów, stąd
  bardzo często umieszczam odwołanie do zewnętrznego arkuszu stylów - public/custom.css. Korzystajcie z tego.)
* Pętle. Jeśli jeden blok występuje w kilku wariacjach - np blok oceny jakichś produktów, to dlaczego by nie wykorzystać tego faktu w prostym skrypcie?
* Debugowanie - szukanie błędów to też coś co zabiera czas. Dobrze by było je wyłapywać i informować o problemie na jak najwcześniejszym etapie</li>

  ```python
      # trochę oswajania z pythonem.
      from kparser import parse
      
      input_ = "Q S Q1 COS"   # to jest to co byście wkleili w okienko parsera
      
      survey = parse(input_)  # a to by się dzialo w tle
      survey.to_xml()
      
      # i gdzieś tam na stronie wyswietliłaby się informacja podobna do tej:
      >> ... ValueError: ('Brak kafeterii w pytaniu ', 'Q1')
  ```

<a name="elementy-minijęzyka"></a>

<a name="mini-język-ankiet"></a>
# Mini język ankiet

Na podstawie przygotowanego wejścia - skryptu minijęzyka - parser przygotowuje odpowiednie wyjście.
Aby parser zadziałał prawidłowo wejście musi być skonstruowane zgodnie z regułami mini języka.

Parser zwraca w zależności od wywołania albo dokument xml reprezentujący survey, albo literał odpowiadający zawartości metada/routingu w mdd (dimensions).

W przyszłości możliwe jest dodanie kolejnych wyjść.


<a name="bloki"></a>
## Bloki

<a name="najprostsze-wywołanie"></a>
### Najprostsze wywołanie.

  ```
  B B0
  ```
  ```xml
  &lt;survey createtime="1438954287629" creator="CHANGEIT" exitpage="" layoutid="ShadesOfGray" localeCode="pl" name="CHANGEIT" sensitive="false" showbar="false" time="60000" SMSComp="false"&gt;
    &lt;block id="BO" name="" quoted="false" random="false" rotation="false"/&gt;
    &lt;vars/&gt;
    &lt;procedures&gt;
      &lt;procedure id="PROC" shortdesc=""/&gt;
    &lt;/procedures&gt;
  &lt;/survey&gt;
  ```

<a name="rotacja-randomizacja"></a>
### Rotacja-Randomizacja

Rotacja:

  ```
  B B0 --rot
  ```

  ```xml
  ...
    &lt;block id="BO" name="" quoted="false" random="false" rotation="true"/&gt;
  ...

  ```

Randomizacja:
	
```
B B0 --ran
```

```xml
...
  &lt;block id="BO" name="" quoted="false" random="true" rotation="false"/&gt;
...
```

A może to i to?
	
  ```B B0 --ran --rot```
  ```python
  ...
    AttributeError: ('Błąd w linii', 'B BO --ran --rot')  # no tak to się nie powinno udać.
  ...
  ```

<a name="zagnieżdzanie"></a>
### Zagnieżdzanie
	
```
B B0 --ran
B B1 B0
B B2 B0
B B3
```


```xml
...
  &lt;block id="B0" name="" quoted="false" random="true" rotation="false"&gt;
    &lt;block id="B1" name="" quoted="false" random="false" rotation="false"/&gt;
    &lt;block id="B2" name="" quoted="false" random="false" rotation="false"/&gt;
  &lt;/block&gt;
  &lt;block id="B3" name="" quoted="false" random="false" rotation="false"/&gt;
...
```

<a name="precode-postocde"></a>
### precode postocde
	
```
B B0
PRE $A="1"
POST $A="2"
```

```xml
...
  &lt;block id="B0" name="" quoted="false" random="false" rotation="false"&gt;
    &lt;precode&gt;&lt;![CDATA[$A="1"]]&gt;&lt;/precode&gt;
    &lt;postcode&gt;&lt;![CDATA[$A="2"]]&gt;&lt;/postcode&gt;
  &lt;/block&gt;
...
```

<a name="prosta-kontrola-ifów-w-precodepostcode"></a>
### Prosta kontrola ifów w precode/postcode

* Błąd w precode:	
```
B B0
PRE if($A1=="1");goto next;endif
POST $A="2"
```

```python
...
ValueError: Błąd w precode elementu B0, Liczba if, else, endif nie zgadza się
```

* Błąd w postcode
	
```
B B0
PRE $A="2"
POST if($A1=="1");goto next;endif
```
```python
...
ValueError: Błąd w postcode elementu B0, Liczba if, else, endif nie zgadza się
```

**Ta kontrola polega jedynie na zliczaniu if/else/endif - jeśli ich liczby się zgadzają to błędu nie rzuci...**


<a name="page"></a>
## Page

Page to taki element, który przydaje się tylko czasem. Najczęściej nie ma sensu deklarować go pisać explicite

Zapis:
```
P Q1_p
Q L Q1 COS
```

Jest równoważny temu:
```
Q L Q1 COS
```

Czasem jednak się przydaje - np wtedy gdy z jakichś względów id page ma być zbudowane od czegoś innego niż id  question

```
P P1
Q L Q1 COS
```

```xml
    &lt;page id="P0" hideBackButton="false" name=""&gt;
      &lt;question id="Q1" name=""&gt;
        &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
          &lt;content&gt;COS&lt;/content&gt;
        &lt;/control_layout&gt;
      &lt;/question&gt;
    &lt;/page&gt;
```
<a name="zagnieżdzanie-1"></a>
### Zagnieżdzanie   
Najbardziej jednak przydaje się przy zagnieżdżaniu
	
```
B B0
B B1 B0
Q L Q1 COS
P P0 --parent:B0
```

```xml
&lt;block id="B0" name="" quoted="false" random="false" rotation="false"&gt;
  &lt;block id="B1" name="" quoted="false" random="false" rotation="false"&gt;
    &lt;page id="Q1_p" hideBackButton="false" name=""&gt;
      &lt;question id="Q1" name=""&gt;
        &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
          &lt;content&gt;COS&lt;/content&gt;
        &lt;/control_layout&gt;
      &lt;/question&gt;
    &lt;/page&gt;
  &lt;/block&gt;
  &lt;page id="P0" hideBackButton="false" name=""/&gt;
&lt;/block&gt;
```
```
B B0
B B1 B0
Q L Q1 COS
P P0
```

```xml
&lt;block id="B0" name="" quoted="false" random="false" rotation="false"&gt;
    &lt;block id="B1" name="" quoted="false" random="false" rotation="false"&gt;
      &lt;page id="Q1_p" hideBackButton="false" name=""&gt;
        &lt;question id="Q1" name=""&gt;
          &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
            &lt;content&gt;COS&lt;/content&gt;
          &lt;/control_layout&gt;
        &lt;/question&gt;
      &lt;/page&gt;
	  &lt;page id="P0" hideBackButton="false" name=""/&gt;
  &lt;/block&gt;
&lt;/block&gt;
```
<a name="questions"></a>
## Questions

Questions to najważniejsza struktura. To tutaj najwięcej się dzieje.

Ogólna konstrukcja pytania jest zawsze taka sama:
```
//1 2 3  4     5 
Q TYP ID TRESC --markery
PRE
POST
kafeteria     //6
_             //7
stwierdzenia  //
```
Jak więc widać jest to konstrukcja wieloliniowa. I warto pamiętać o kilku regułach:
* pomiędzy 1 2 3 4 5 - pojedyńcze spacje
* kafeteria zawsze pod pytaniem (albo po precode/postcode)
* kafeterię i stwierdzenia oddziela _


| 2         | Wartości                                                                                   |
|-----------|--------------------------------------------------------------------------------------------|
| TYP       | S,M,L,N,O,LHS,B,SDG,G,B,T,SLIDER,SLIDERS,H,R,CS                                            |
| --markers | --images, --listcolumn, --dezaktywacja, --minchoose:xx, --maxchoose:xx, --nr, --custom_css |


Do tego w kafeterii można stosować:

* przy id:
  * .d - dezaktywacja
  * .c - podłączony open

* po treści, jako dodatkowe markery:

| Marker         | Akcja      | Dodatkowy opis                                      |
|----------------|------------|-----------------------------------------------------|
| --so           | screen out | na postcode strony: #OUT = "1";goto KONKURS         |
| --gn           | goto next  | precode następnej strony: if z goto next            |
| --goto:id      | goto id    | na postcode strony: if z goto id                    |
| --hide:pattern | hide       | Dodaje do list_item hide. Działa też dla stwierdzeń |

<a name="kilka-pytań-na-stronie"></a>
### Kilka pytań na stronie

Aby wywołać kilka pytań na stronie należy przy wywołaniu pytania dodać parametr --p:

przykładowe wywołanie:
```
P P0
Q O qtest_st --p:P0 st
Q O qtest_rt --p:P0 rt
Q O qtest_at --p:P0 at
Q O qtest_nt --p:P0 nt
```

inny przykład:
```
B B0
Q O Q1 A
Q O Q2 --p:Q1_p B
```

```xml
&lt;page id="Q1_p" hideBackButton="false" name=""&gt;
  &lt;question id="Q1" name=""&gt;
    &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
      &lt;content&gt;A&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_open id="Q1" length="25" lines="1" mask=".*" name="Q1 | A" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_open&gt;
  &lt;/question&gt;
  &lt;question id="Q2" name=""&gt;
    &lt;control_layout id="Q2.labelka" layout="default" style=""&gt;
      &lt;content&gt;B&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_open id="Q2" length="25" lines="1" mask=".*" name="Q2 | B" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_open&gt;
  &lt;/question&gt;
&lt;/page&gt;
```

    
<a name="singlemulti---co-można-w-nich-zautomatyzować"></a>
## Single/Multi - co można w nich zautomatyzować?
    
```
Q S Q1 COS --ran--images
a
b
c
96.c Inne
97.d Nie wiem

Q S Q2 COS --images
a --hide:$Q1:{0} == "0"
b
c
96 $Q1_96T$
97.d Nie wiem --hide:"0"
```

```xml
...

&lt;page id="Q2_p" hideBackButton="false" name=""&gt;
  &lt;question id="Q2" name=""&gt;
    &lt;control_layout id="Q2.labelka" layout="default" style=""&gt;
      &lt;content&gt;COS &lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_single id="Q2" layout="vertical" style="" itemlimit="0" name="Q2 | COS " random="false" require="true" results="true" rotation="false"&gt;
      &lt;list_item id="1" name="" style=""&gt;
        &lt;content&gt;a&lt;/content&gt;
        &lt;hide&gt;&lt;![CDATA[$Q1:1 == "0"]]&gt;&lt;/hide&gt;
      &lt;/list_item&gt;
      ...
      &lt;list_item id="96" name="" style=""&gt;
        &lt;content&gt;$Q1_96T$&lt;/content&gt;
        &lt;hide&gt;&lt;![CDATA[$Q1:96 == "0"]]&gt;&lt;/hide&gt;
      &lt;/list_item&gt;
      &lt;list_item id="97" name="" style="" disablerest="true"&gt;
        &lt;content&gt;Nie wiem&lt;/content&gt;
        &lt;hide&gt;&lt;![CDATA["0"]]&gt;&lt;/hide&gt;
      &lt;/list_item&gt;
    &lt;/control_single&gt;
    &lt;control_layout id="Q1.js" layout="default" style=""&gt;
      &lt;content&gt;
        &lt;!-- Obrazki zamiast kafeterii --&gt;
        &lt;script type=\'text/javascript\'&gt;
          var multiImageControlId = \'Q1\';
        &lt;/script&gt;
      &lt;/content&gt;
    &lt;/control_layout&gt;
  &lt;/question&gt;
&lt;/page&gt;
```

<a name="dodatkowe-skróty-w-singlemulti"></a>
## Dodatkowe skróty w Single/Multi?
    
```
Q S Q1 COS
a --so
b --gn
c --goto: Q10_p

Q L Q2 COS
```

```xml
...
&lt;block id="Default" name="" quoted="false" random="false" rotation="false"&gt;
  &lt;page id="Q1_p" hideBackButton="false" name=""&gt;
    &lt;question id="Q1" name=""&gt;
      &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
        &lt;content&gt;COS&lt;/content&gt;
      &lt;/control_layout&gt;
      &lt;control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS" random="false" require="true" results="true" rotation="false"&gt;
        &lt;list_item id="1" name="" style=""&gt;
          &lt;content&gt;a&lt;/content&gt;
        &lt;/list_item&gt;
        &lt;list_item id="2" name="" style=""&gt;
          &lt;content&gt;b&lt;/content&gt;
        &lt;/list_item&gt;
        &lt;list_item id="3" name="" style=""&gt;
          &lt;content&gt;c &lt;/content&gt;
        &lt;/list_item&gt;
      &lt;/control_single&gt;
    &lt;/question&gt;
    &lt;postcode&gt;&lt;![CDATA[
if ($Q1:1 == "1")
&#35;OUT = "1"
goto KONKURS
else
endif
]]&gt;&lt;/postcode&gt;
    &lt;/page&gt;
    &lt;page id="Q2_p" hideBackButton="false" name=""&gt;
      &lt;precode&gt;&lt;![CDATA[if ($Q1:2 == "1")
    goto next
else
endif

if ($Q1:3 == "1")
    goto Q10_p
else
endif]]&gt;&lt;/precode&gt;
    &lt;question id="Q2" name=""&gt;
      &lt;control_layout id="Q2.labelka" layout="default" style=""&gt;
        &lt;content&gt;COS&lt;/content&gt;
      &lt;/control_layout&gt;
    &lt;/question&gt;
  &lt;/page&gt;
&lt;/block&gt;

```

**Cześć kodu pojawia się na precode następnej strony - goto next nie ma sensu na postocde.**
    
<a name="multi---minchoosemaxchoose"></a>
## Multi - minchoose/maxchoose

W kontrolkach multi dodatkowo możemy określić minimalna i maksymalną ilość wskzań

```
Q M Q1 COS--minchoose:2--maxchoose:2
A
B
C
```

```xml
&lt;control_multi id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS" random="false" require="true" results="true" rotation="false" minchoose="2" maxchoose="2"&gt;
  &lt;list_item id="1" name="" style=""&gt;
	&lt;content&gt;A&lt;/content&gt;
  &lt;/list_item&gt;
  &lt;list_item id="2" name="" style=""&gt;
	&lt;content&gt;B&lt;/content&gt;
  &lt;/list_item&gt;
  &lt;list_item id="3" name="" style=""&gt;
	&lt;content&gt;C&lt;/content&gt;
  &lt;/list_item&gt;
&lt;/control_multi&gt;
```

<a name="python"></a>
# Python
I to jest dobry czas by się na chwile zatrzymać i zająć innym tematem. W dalszej części wyjaśni się dlaczego.

<a name="first-blood"></a>
## First blood

Python to język interpretowany, skryptowy o szerokim wahlarzu zastosowań. Znaleźć go można niemal wszędzie.<br>
W tym miejscu nie skupiamy się na nauce pythona, ale umówmy się - nikomu by to nie zaszkodziło.
Im więcej języków znasz tym lepiej dla Ciebie. Kropka.

* [www.python.org] (https://www.python.org) - najważniejsze pythonowe miejsce w sieci
* [pl.python.org] (https://pl.python.org/) - dużo informacji i kursów, w tym po polsku

Jeśli zdecydujesz się i zainstalujesz pythona, to po wpisaniu w terminalu (command line) komendy python uruchomi Ci się interpreter. Poznasz to po znaku zachęty:

```python
Python 3.4.0 (default, Jun 19 2015, 14:20:21)
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

```

**W dalszej częsci pojawi się kilka przykładów z interpretera.**


Jeśli korzystasz z parsera na stronie, to właściwie nawet nie musisz instalować Pythona.
W dalszej części po prostu postaram Ci się wytłumaczyć to co trzeba wiedzieć by tworzyć efektywnie skrypty. W szczególności będzie to dotyczyć
klauzuli
```
BEGIN PROGRAM
END PROGRAM
```

<a name="python---zmienne"></a>
## Python - zmienne

Zmienne w pythonie mogą mieć różne typy
```python
>>> x=1
>>> type(x)
&lt;class 'int'&gt;
>>> y=2.2
>>> type(y)
&lt;class 'float'&gt;
>>> x+y
3.2
>>> x*y
2.2
>>> x/y
0.45454545454545453
>>> y=True
>>> type(z)
&lt;class 'bool'&gt;
>>> n=False
>>> n and y
False
>>> n or y
True
>>> pattern = '$Q1:{0} == "0" '
>>> type(pattern)
&lt;class 'str'&gt;
>>> "Ala"+ " ma kota."
'Ala ma kota'
>>> "Ala"*3
'AlaAlaAla'
&#35; łańcuchy tekstowe mają różne fajne metody. Jedną z nich jest format,
>>> pattern.format(1)   # Mniej więcej w ten sposób ogarniany jest dynamicznie tworzony hide list itemów
'$Q1:1 == "0" '
>>> pattern.split(' == ')
['$Q1:1', '"0" ']
>>> string_ktory_ma_wiele_linii = '''B B0_1
Q L Q1_1 COS
Q L Q1_2 COS
Q L Q1_3 COS'''
```

<a name="python---stringformat"></a>
## Python - string.format()

** Format jest bardzo przydatną metodą. Często przydaje w tworzeniu bloków tekstu. ** 

```python
&#35; różne przykłady użycia funkcji format
>>> tekst = "On ma na imie {0} i wygląda na {1} lat"
>>> tekst1 = tekst.format("Wiktor", 50)
>>> tekst2 = tekst.format("Paweł", "25")
>>> print(tekst1+'.' , tekst2)
On ma na imie Wiktor i wygląda na 50 lat. On ma na imie Wiktor i wygląda na 50 lat
```

```python
>>> &#35; tych miejsc nie trzeba nawet numerować, o ile się nie powtarzają
>>> tekst3 = "On ma na imie {} i zachowuje się jakby miał {} lat"
>>> imie, lat = "Patryk", 5
>>> tekst4 = tekst3.format(imie, lat)
>>> print(tekst4)
```


```python
tekst5 = "On ma na imie {} i zachowuje się jakby miał {} lat a nie ma {} lat"
tekst6 = tekst5.format(imie, lat)
...
IndexError: tuple index out of range
```

```python
>>> string_ktory_ma_wiele_linii = '''
B B_Q1 B0
Q L Q1_{0}_1 COS
Q L Q1_{0}_2 COS
Q L Q1_{0}_3 COS'''
>>> x = string_ktory_ma_wiele_linii.format(1)
>>> x
'\nB B_Q1 B0 \nQ L Q1_10_1 COS\nQ L Q1_10_2 COS\nQ L Q1_10_3 COS'
>>> print(x)
```

```
B B_Q1 B0
Q L Q1_10_1 COS
Q L Q1_10_2 COS
Q L Q1_10_3 COS
```


```python
>>> &#35; jest tylko jeden myk - jeśli w tekście sa {} to trzeba je dublować {{""}}
>>> text = "hl = new IbisHighlighter('{0}.img','{0}.input', \{\{ hlClass: 'hl-active-green', debug: false \}\})".format('Q1')
"hl = new IbisHighlighter('Q1.img','Q1.input', { hlClass: 'hl-active-green', debug: false })"
```

<a name="python---listy-i-słowniki"></a>
## Python - listy i słowniki

* Lista - zbiór uporządkowanych elementów, które mogą być różnego rodzaju

```python
>>> l = []  # pusta lista
>>> type(l)
&lt;class 'list'&gt;
>>> l2 = ['a', 1, 'cos', [1,2,3]] # lista różnych elementów
>>> l2
['a', 1, 'cos', [1, 2, 3]]
>>> l2[0]  # pierwszy element
'a'
>>> l2[-1] # ostatni
[1, 2, 3]
>>> l2[1:3] # wycinek listy
[1, 'cos']
>>> len(l2)  # długość listy
4
>>> l2.index('cos')  # index zadanego elementu
2
>>> l2[::-1] # odwrócona lista
[[1, 2, 3], 'cos', 1, 'a']
```
Oczywiście to nie wszystko. Do list można dodawać, elementy, usuwać, zmieniać. listy można łączyć, listy można odwracać, sortować, dzielić, wyszukiwać w nich elementy i milion innych rzeczy. Dla nas ważne jest to, by wiedzieć, że listy są i jak je stworzyć
```python
>>> &#35; Łatwo sprawdzić jakie metody są dostępne dla naszego obiektu:
>>> dir(l2)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__',
'__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__',
'__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__',
'__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop',
'remove', 'reverse', 'sort']
>>> &#35; można też użyć wbudowanej metody help: help(l2) lub bardziej konkretnie help(l2.pop)
```

* Słowniki - to z koleji zbiór, który nie jest uporządkowany. Ale za to ma inną zajebistą cechę - a mianowicie klucz i wartość mu odpowiadającą

```python
>>> imiona_dopelniacz = {"Wiktor": "Wiktora"}
>>> imiona_dopelniacz['Edyta'] = "Edyty"
>>> imiona_dopelniacz
{'Edyta': 'Edyty', 'Wiktor': 'Wiktora'}
>>> imiona_dopelniacz['Wiktor']
'Wiktora'
```

Wracając do przykładu z formatowaniem tekstu. Tu czasem przydatny jest słownik. Szczególnie, gdy jest ich dużo i chcemy łątwo się domyślać gdzie co wstawić
```python
&#35; poprawmy trochę ten przykład
>>> slownik = {"imie": "Patryk", 'wiek': "5"}
>>> tekst5 = "On ma na imie {imie} i zachowuje się jakby miał {wiek} lat a nie ma {wiek} lat"
>>> tekst6 = tekst5.format(**slownik)
>>> print(tekst6)
On ma na imie Patryk i zachowuje się jakby miał 5 lat a nie ma 5 lat
```

<a name="python---pętle"></a>
## Python - pętle

Python dostarcza kilku rodzajów pętli. W naszej praktyce najczęściej korzysta się z pętli for. I tu pojawia się w końcu ważna koncepcja pythona - indentancja, czyli wcięcia. Weźmy sobie przykład pętli for:

```python
>>> x = 'ala'
>>> &#35; dobrze
>>> for i in x:
...     i = i*2
...     print(i)
...
aa
ll
aa
>>> &#35; źle
>>> for i in x:
...  i = i*2
...   print(i)
  File "&lt;stdin&gt;", line 3
    print(i)
    ^
IndentationError: unexpected indent
```

* Tworząc w mini języku wstawki z pythona należy o tym pamiętać. Wcięcia mogą być właściwie dowolne, ale muszą być w całym kodzie konsekwentnie stosowane.
* Zgodnie ze standardem PEP8 najlepiej jest stosować 4 spacje
* Pętlę for można stosować na wszelkiego rodzaju iterowalnych zbiorach. Jeśli ten zbiór nazywa się x to piszemy <code>for i in x:</code>.

```python
>>> x = ['a', 'b', 'c']
>>> for count, i in enumerate(x):  # enumerate to przydatna metoda - zwraca nam parę index, element
...     print(i*count)
...

b
cc
>>> for i in range(3):  # range można też wywołać np tak range(1, 11) - stworzy to listę 1, ... ,10
...     print(i)
0
1
2
>>> my_dict = {'1': 'a', '2': 'z'}
>>> for key in my_dict.keys():
...     print(my_dict[key])
z   # no właśnie - tu kolejnośc może być różna
a
>>> &#35; jeśli chcemy uporządkowany słownik, to trzeba zrobić tak:
>>> from collections import OrderedDict  # i tu mamy przykład importu
>>> my_dict = OrderedDict()
>>> my_dict['1'] = "a"
>>> my_dict['2'] = "z"
>>> for key in my_dict.keys():
	print(my_dict[key])
a
z
>>>
```

<a name="funkcje-i-klasy"></a>
## Funkcje i klasy
Python to język, który umożliwia stosowanie różnych paradygmatów programowania - np programowanie obiektowe, funkcyjne.

<a name="funkcje"></a>
### Funkcje
```python
def funkcja_ktora_nic_nie_robi():
    pass

>>> funkcja_ktora_nic_nie_robi()
>>>
>>> print(funkcja_ktora_nic_nie_robi())
None

def nazwa_funkcji(argument1, argument2):
    """To jest docstring. Opisuje co funkcja robi."""
    # mozna coś tu zrobić z argumentami
    wynik = argument1 + ' ' + argument2
    return wynik
>>> x = nazwa_funkcji('a', 'b')
>>> x
'a b'
```

<a name="klasy"></a>
### Klasy

```python
class Wspolrzedne():
    def __init__(self, x, y):
        """Inicjuje instancję klasy z zadanymi parametrami"""
        self.x = x
        self.y = y

    def __str__(self):   # potrzebna np do print
        """Reprezentacja tekstowa współrzędnych"""
        return "x={0}, y={1}".format(self.x, self.y)

    def change(self, x, y):
        """Zmiana współrzędnych"""
        self.x += x
        self.y += y
        print(self)
>>> my_position = Wspolrzedne(0,0)
>>> print(my_position)
x=0, y=0
>>> my_position.change(1,2)
x=1, y=2
```

<a name="mini-język-cd"></a>
# Mini język cd...

<a name="klauzula-begin-program--end-program"></a>
## klauzula BEGIN PROGRAM / END PROGRAM

Założmy.. zupełnie hipotetycznie, że mamy stworzyć losowanie złożone z 100 stron

```
B LOSOWANIE --ran
Q L LOS_1 LOS
PRE if(#ILE>"10");goto next;else;endif;;#POKAZ_1 = "1";#ILE = [#ILE + "1"]; goto next;
```

Jak się do tego zabrać:
* no można ręcznie... ale 100 stron? 
* Można w Excelu albo jakimś języku programowania.. potem wkleić, skleić i gotowe.
* Ale można też tak:

```
B LOSOWANIE --ran
BEGIN PROGRAM
def func():
    x = ""  # pusty string, będę go powiększać o nowe elementy

	temp = '''Q L LOS_{0} LOS
PRE if(#ILE>"10");goto next;else;endif;;#POKAZ_{0} = "1";#ILE = [#ILE + "1"]; goto next;
'''
    for i in range(1, 101):
        x += temp.format(x)  # to już znamy
    return x
xxx = func()  # coś takiego musi być by odczytywała sie wartość tej wywołanej funkcji
END PROGRAM
```

```xml
  &lt;block id="LOSOWANIE" name="" quoted="false" random="true" rotation="false"&gt;
    &lt;page id="LOS_1_p" hideBackButton="false" name=""&gt;
      &lt;precode&gt;&lt;![CDATA[...
&#35;POKAZ_1 = "1"
...
]]&gt;&lt;/precode&gt;
...
    &lt;page id="LOS_100_p" hideBackButton="false" name=""&gt;
      &lt;precode&gt;&lt;![CDATA[...
&#35;POKAZ_100 = "1"
...
]]&gt;&lt;/precode&gt;
...
```

To co się dzieje w funkcji func() to już jest naprawdę zupełnie dowolne - można tam wykonać właściwie każdy kod pythona.
**Ważne jest by funkcja ta zwróciła poprawny fragment parsera**. Można tam sobie naprawde dowolnie iterować po różnych listach, formatować tekst, dla różnych przypadków itd


<a name="kontrolka-open"></a>
## Kontrolka Open

```
Q O90_4 Q1 COS
```
```xml
&lt;page id="Q1_p" hideBackButton="false" name=""&gt;
  &lt;question id="Q1" name=""&gt;
    &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
      &lt;content&gt;COS&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_open id="Q1" length="90" lines="4" mask=".*" name="Q1 | COS" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_open&gt;
  &lt;/question&gt;
&lt;/page&gt;
```

```
Q O90_4 Q1 COS--nr
1
2
```

```xml
...
&lt;control_open id="Q1_1" length="25" lines="1" mask=".*" name="Q1_1 | 1" require="false" results="true" style=""&gt;
  &lt;content/&gt;
&lt;/control_open&gt;
&lt;control_open id="Q1_2" length="25" lines="1" mask=".*" name="Q1_2 | 2" require="false" results="true" style=""&gt;
  &lt;content/&gt;
&lt;/control_open&gt;
...
```

```
Q O90_4 Q1 COS --dk: Nie wiem
```

```xml
...
       &lt;control_open id="Q1" length="90" lines="4" mask=".*" name="Q1 | COS " require="true" results="true" style=""&gt;
          &lt;content/&gt;
        &lt;/control_open&gt;
        &lt;control_layout id="Q1.js" layout="default" style=""&gt;
          &lt;content&gt;
&lt;!-- dezaktywacja opena --&gt;
&lt;script type=\'text/javascript\'&gt;
    var opendisDest = "Q1";
    var opendisText = "Nie wiem";
    var opendisValue = "98";
&lt;/script&gt;
&lt;script type=\'text/javascript\' src=\'opendis/opendis.js\'&gt;&lt;/script&gt;
&lt;/content&gt;
        &lt;/control_layout&gt;
...
```

<a name="numeric"></a>
## Numeric

Analogicznie w sumie jest dla Number - tyle że wywołanie to: <code>Q N Q1 COS</code></h3>


<a name="tabelka-js"></a>
## Tabelka JS

Najprostszy przypadek

```
Q T Q1 COS
1 A
2 B
_
2 B
```

**Zawsze pierwsza jest kafeteria, a potem stwierdzenia**

Dość złożony przypadek
```
Q T Q1 COS --multi
1 A --hide:$S1:{0} == "0"
2 B
_
2 B --hide:$Q1:{0} == "1"
```

Musi być też niestety ta spacja przed --hide - z czasem to dopracujemy.
--multi oznacza, że kafeteria to będą kontrolki multi

<a name="slider"></a>
## Slider

```
Q SLIDER Q1 TRESC
```

Tworzy po prostu numerica i wywołanie skryptu


```
Q SLIDER Q1 TRESC
lewy koniec
prawy koniec
```

Ubiera to w tabelkę kreaturową z opisami końców skali


<a name="sliders"></a>
## Sliders


```
Q SLIDERS Q1 TRESC
Lewy koniec
Prawy koniec
_
A
B
C
```

Tworzy tabelę kreaturową:
A | lewy koniec | numeric | prawy koniec

Dodaje wywołanie skryptów

Opcjonalnie można wywołać z opcją --ran
```
Q SLIDERS Q1 TRESC --ran
Lewy koniec
Prawy koniec
_
A
B
C
```
wtedy tabelki na ekranie będą randomizowane/
Uwaga! Do randomizacji tabelek jest specjalny skrypt

jego wywołanie jest ujęte przy wywołaniu skrypty. Opcjonalnie można zaciągnąć go bezpośrednio z githuba, 
lepiej jednak nie robić tego na produkcji.

  ```html
  <script type='text/javascript' src='public/rotate_tables.js'></script>
  <!-- get the file from https://github.com/rkorzen/ibisjs
       optionally uncomment the line bellow (only for tests - never for production!!)
  <script type='text/javascript' src='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.js'></script>
  <link rel='stylesheet' href='https://rawgit.com/rkorzen/ibisjs/master/rotate_tables.css' type='text/css'>-->
  ```



<a name="gridy"></a>
## Gridy

```
Q G Q1 COS
1 a
_
1 stw a
```

Domyślnym typem kafeterii jest single. By użyć multi należy

```
// Q SDG Q1 COS--maxchoose:5  <- tak też można
Q G Q1 COS--maxchoose:5
1 a
2 b
_
1 stw a--multi --hide:$A1:{0}=="1"
```

dla stw 1 będzie multi. Ponadto ustawiamy maxchoose dla multi na 5 - co akurat w tym przypadku jest bez sensu

<a name="koszyczki"></a>
## Koszyczki

Zwykły koszyczek

```
// Q LHS Q1 COS
Q B Q1 COS
1 1
2 2
_
1 A
2 B
```

```xml
&lt;page id="Q1_p" hideBackButton="false" name=""&gt;
  &lt;question id="Q1" name=""&gt;
    &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
      &lt;content&gt;&lt;div class="basket_instrukcja"&gt;COS&lt;/div&gt;&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_single id="Q1" layout="vertical" style="" itemlimit="0" name="COS" random="false" require="false" results="true" rotation="false"&gt;
      &lt;list_item id="1" name="" style=""&gt;
        &lt;content&gt;&lt;img src="public/Q1/1.jpg" alt = "1"&gt;&lt;/content&gt;
      &lt;/list_item&gt;
...
    &lt;control_multi id="Q1x1" layout="vertical" style="" itemlimit="0" name="Q1x1 | A" random="false" require="false" results="true" rotation="false"&gt;
      &lt;list_item id="1" name="" style=""&gt;
        &lt;content&gt;&lt;img src="public/Q1/1.jpg" alt = "1"&gt;&lt;/content&gt;
      &lt;/list_item&gt;
...
&lt;control_multi id="Q1x2" layout="vertical" style="" itemlimit="0" name="Q1x2 | B" random="false" require="false" results="true" rotation="false"&gt;
...
    &lt;control_layout id="Q1.js" layout="default" style=""&gt;
      &lt;content&gt;&lt;!-- Baskets --&gt;
...
&lt;script type="text/javascript"&gt;
var bm = new BasketManager({className: "multi", dest: "Q1"});
bm.createBasket("Q1", {
source: true,
max: 0
});
bm.createBasket("Q1x1", {
label: "A",
min: 0,
max: 2,
maxreplace: true
});
...
&lt;/script&gt;
&lt;link rel="stylesheet" href="public/custom.css" type="text/css"&gt;&lt;/content&gt;
...
```

Inne możliwe wywołanie to np - analogicznie jak w single/multi 

```
Q B Q1 COS --ran
1 a
_
1 a
```
Można też stosować hide dla kafeterii

<a name="highlighter"></a>
## Highlighter

Wywołując musimy pamiętać po podaniu ścieżki do obrazka. Jeśli obrazka nie podacie dostaniecie błąd

```
Q H Q1 COS
```

```python
ValueError: ('Highlighter wymaga podania obrazka, lokalizacje obrazka bez znacznikówhtml umiesc  jako pierwszy element kafeterii', 'Q1')
```

Poprawne wywołanie
```
Q H Q1 COS
public/X4_2.jpg
```

```xml
&lt;page id="Q1_p" hideBackButton="false" name=""&gt;
  &lt;question id="Q1" name=""&gt;
    &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
      &lt;content&gt;COS&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_layout id="Q1.js" layout="default" style=""&gt;
      &lt;content&gt;&lt;script type=\'text/javascript\' src=\'public/highlighter/highlighter.js\'&gt;&lt;/script&gt;
&lt;link rel=\'stylesheet\' type=\'text/css\' href=\'public/highlighter/highlighter.css\'/&gt;
&lt;script type=\'text/javascript\'&gt;
hl = new IbisHighlighter(\'Q1.img\',\'Q1.input\', { hlClass: \'hl-active-green\', debug: false })
&lt;/script&gt;&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_layout id="Q1.img" layout="default" style=""&gt;
      &lt;content&gt;&lt;img src="public/X4_2.jpg"&gt;&lt;/content&gt;
    &lt;/control_layout&gt;
    &lt;control_open id="Q1.input" length="25" lines="1" mask=".*" name="Q1.input" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_open&gt;
  &lt;/question&gt;
&lt;/page&gt;
```

<a name="ranking"></a>
## Ranking

Wywołując musimy pamiętać o tym, że id caf NIE MOGĄ MIEĆ ZER WIODĄCYCH
```
Q R Q1 COS
01 a
b

```

```python
ValueError: W rankingu Q1 w kafeterii nie może być zer wiodących
```

```
Q R Q1 COS
a
b
```
```xml
&lt;page id="Q1_p"&gt;
  &lt;question id="Q1instr"&gt;
    &lt;control_layout id="Q1_lab_instr" layout="default" style=""&gt;
      &lt;content&gt;&lt;div class="ranking_instrukcja"&gt;COS&lt;/div&gt;&lt;/content&gt;
    &lt;/control_layout&gt;
  &lt;/question&gt;
  &lt;question id="Q1"&gt;
    &lt;control_single id="Q1" layout="vertical" style="" itemlimit="0" name="Q1 | COS" random="false" require="false" results="true" rotation="false"&gt;
      &lt;list_item id="1" name="" style=""&gt;
        &lt;content&gt;a&lt;/content&gt;
      &lt;/list_item&gt;
      &lt;list_item id="2" name="" style=""&gt;
        &lt;content&gt;b&lt;/content&gt;
      &lt;/list_item&gt;
    &lt;/control_single&gt;
    &lt;control_number id="Q1.number1" float="false" mask=".*" name="Pozycja Odp1" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_number&gt;
    &lt;control_number id="Q1.number2" float="false" mask=".*" name="Pozycja Odp2" require="true" results="true" style=""&gt;
      &lt;content/&gt;
    &lt;/control_number&gt;
    &lt;control_layout id="Q1.js" layout="default" style=""&gt;
      &lt;content&gt;&lt;!-- Script Ranking --&gt;
&lt;link rel=stylesheet type=text/css href="public/ranking.css"&gt;
&lt;script type=\'text/javascript\' src=\'public/jquery-ui-1.7.2.custom.min.js\'&gt;&lt;/script&gt;
&lt;script type=\'text/javascript\' src=\'public/ranking.js\'&gt;&lt;/script&gt;
&lt;script type=\'text/javascript\'&gt;addRanking("Q1");&lt;/script&gt;
&lt;!-- end Script Ranking --&gt;

&lt;link rel=stylesheet type=text/css href="public/custom.css"&gt;&lt;/content&gt;
    &lt;/control_layout&gt;
  &lt;/question&gt;
&lt;/page&gt;
```


<a name="conceptselect"></a>
## ConceptSelect

**Uwaga!** Tag nowej lini &lt;br&gt; powinien być "przyklejony" do ostatniego słowa linii
Wejście tekstowe jest dzielone po spacjach, więc spacje trzeba używać rozsądnie.
Wszelkie znaczniki html powinny być poprzyklejane!

Wywołanie

```
Q CS Q1 COS
a b c
```

```xml
    &lt;page id="Q1_p" hideBackButton="false" name=""&gt;
      &lt;question id="Q1" name=""&gt;
        &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
          &lt;content&gt;CO&#347;&lt;/content&gt;
        &lt;/control_layout&gt;
        &lt;control_layout id="Q1_tresc" layout="default" style=""&gt;
          &lt;content&gt;a | b | c&lt;/content&gt;
        &lt;/control_layout&gt;
        &lt;control_open id="Q1_data" length="25" lines="1" mask=".*" name="Q1_data | ConceptSelect" require="true" results="true" style="display:none;"&gt;
          &lt;content/&gt;
        &lt;/control_open&gt;
        &lt;control_multi id="Q1_dis" layout="vertical" style="" itemlimit="0" name="Q1_dis" random="false" require="false" results="true" rotation="false"&gt;
          &lt;list_item id="98" name="" style=""&gt;
            &lt;content&gt;Nic nie zwr&#243;ci&#322;o mojej uwagi&lt;/content&gt;
          &lt;/list_item&gt;
        &lt;/control_multi&gt;
        &lt;control_layout id="Q1.js" layout="default" style=""&gt;
          &lt;content&gt;
&amp;lt;!-- Disabler  --&amp;gt;
&amp;lt;script type='text/javascript' src='public/ibisDisabler.js'&amp;gt;&amp;lt;/script&amp;gt;
&amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.98','Q1_tresc');
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&amp;lt;!-- Disabler  --&amp;gt;
&amp;lt;script type='text/javascript' src='public/ibisDisabler.js'&amp;gt;&amp;lt;/script&amp;gt;
&amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.98','Q1_data',98);
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&lt;!-- Concept Select  --&gt;
&lt;link rel="stylesheet" href="public/Selection_sog.css" type="text/css"&gt;
&lt;script type='text/javascript' src='public/Selection_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
var sel = new Selection({
textContainerId: "Q1_tresc",
openContainerId: "Q1_data",
delimiter: "|"
});
&lt;!-- End ConceptSelect --&gt;
&lt;/content&gt;
        &lt;/control_layout&gt;
      &lt;/question&gt;
    &lt;/page&gt;
```

<a name="conceptselect-z-niestandardowym-ibisdisablerem"></a>
## ConceptSelect z niestandardowym IbisDisablerem

Wywołanie z niestandardowym IbisDisablerem
```
Q CS Q1 COS
a b c
_
97 Odmowa
98 Nie wiem
```

```xml
    &lt;page id="Q1_p" hideBackButton="false" name=""&gt;
      &lt;question id="Q1" name=""&gt;
        &lt;control_layout id="Q1.labelka" layout="default" style=""&gt;
          &lt;content&gt;CO&#347;&lt;/content&gt;
        &lt;/control_layout&gt;
        &lt;control_layout id="Q1_tresc" layout="default" style=""&gt;
          &lt;content&gt;a | b | c&lt;/content&gt;
        &lt;/control_layout&gt;
        &lt;control_open id="Q1_data" length="25" lines="1" mask=".*" name="Q1_data | ConceptSelect" require="true" results="true" style="display:none;"&gt;
          &lt;content/&gt;
        &lt;/control_open&gt;
        &lt;control_multi id="Q1_dis" layout="vertical" style="" itemlimit="0" name="Q1_dis" random="false" require="false" results="true" rotation="false"&gt;
          &lt;list_item id="97" name="" style="" disablerest="true"&gt;
            &lt;content&gt;Odmowa&lt;/content&gt;
          &lt;/list_item&gt;
          &lt;list_item id="98" name="" style=""&gt;
            &lt;content&gt;Nie wiem&lt;/content&gt;
          &lt;/list_item&gt;
        &lt;/control_multi&gt;
        &lt;control_layout id="Q1.js" layout="default" style=""&gt;
          &lt;content&gt;
&amp;lt;script type='text/javascript' src='public/ibisDisabler.js'&amp;gt;&amp;lt;/script&amp;gt;
&amp;lt;!-- Disabler  --&amp;gt;
&amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.97','Q1_tresc');
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&amp;lt;!-- Disabler  --&amp;gt;
&amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.97','Q1_data',97);
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&amp;lt;!-- Disabler  --&amp;gt;
&amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.98','Q1_tresc');
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&amp;lt;!-- Disabler  --&amp;gt;
amp;lt;script type='text/javascript'&amp;gt;
setIbisDisabler('Q1_dis.98','Q1_data',98);
&amp;lt;/script&amp;gt;
&amp;lt;!-- End Disabler  --&amp;gt;

&lt;!-- Concept Select  --&gt;
&lt;script type='text/javascript' src='public/Selection_sog.js'&gt;&lt;/script&gt;
&lt;script type='text/javascript'&gt;
var sel = new Selection({
textContainerId: "Q1_tresc",
openContainerId: "Q1_data",
delimiter: "|"
});
&lt;!-- End ConceptSelect --&gt;
&lt;/content&gt;
        &lt;/control_layout&gt;
      &lt;/question&gt;
    &lt;/page&gt;
```


<a name="dimensions"></a>
# Dimensions

```
//to_web or to_dim
B SCREENER
Q S S1 Czy prowadzi Pan(i) zdrowy tryb życia?
1 Tak--so
2 Nie

Q S S5 Czy zdarza się Pan(i) palić papierosy?
1 Tak
2 Nie 

Q S S6 Jakie Pan(i) pali? --ran
PRE if ($S5:1 == "1");else;goto next;endif
1 Mocne
2 Słabe
3 Skręty

BEGIN PROGRAM
lista = """1 Popularne
2 Malboro
3 LM""".splitlines()

def func(lista):
    out = ""
    for x in lista:
        x = x.split(" ", 1)
        out += """
B C2_C6_{0}
Q S C2_{0} W jaki sposób przypala Pan(i) papierosy {2}?
1 Zapałką
2 Zapalniczką
3 Od ogniska
4 Siłą woli
5.c Inaczej, jak...?

Q N C4_{0} Ile średnio licząc pstryknięć wykonuje Pan(i) przypalając {2}?
PRE if($C2_{0}:2 == "1");else;goto next;endif

""".format(x[0], str(int(x[0]) + 1), x[1])
    return out
xxx = func(lista)
END PROGRAM

Q S C7 Czy leki w różnych formach stosuje Pan(i)?
PRE //$C1 count > 2
1 Zazwyczaj wszystkie naraz
2 Osobno - w zależności od objawów

```

<a name="lewa-strona"></a>
## Lewa strona

Abu uzyskać wejśćie do metadata dodaj na początku linię
//to_dim

<a name="podstawy"></a>
### Podstawy

```

    S1 "Czy prowadzi Pan(i) zdrowy tryb życia?"
    Categorical [1..1]
    {
        x1 "Tak",
        x2 "Nie"

    };

    S5 "Czy zdarza się Pan(i) palić papierosy?"
    Categorical [1..1]
    {
        x1 "Tak",
        x2 "Nie"

    };

    S6 "Jakie Pan(i) pali?"
    Categorical [1..1]
    {
        x1 "Mocne",
        x2 "Słabe",
        x3 "Skręty"

    };

    C2_1 "W jaki sposób przypala Pan(i) papierosy Popularne?"
    Categorical [1..1]
    {
        x1 "Zapałką",
        x2 "Zapalniczką",
        x3 "Od ogniska",
        x4 "Siłą woli",
        x5 "Inaczej, jak...?" other

    };

    C4_1 "Ile średnio licząc pstryknięć wykonuje Pan(i) przypalając Popularne?"

    'style(
    '    Width = "3em";
    ')
    'codes(
    '{
    '    - "Nie wiem" DK,
    '    - "Te leki nie są dostępne na receptę" NA
    '}
    long;

    C2_2 "W jaki sposób przypala Pan(i) papierosy Malboro?"
    Categorical [1..1]
    {
        x1 "Zapałką",
        x2 "Zapalniczką",
        x3 "Od ogniska",
        x4 "Siłą woli",
        x5 "Inaczej, jak...?" other

    };

    C4_2 "Ile średnio licząc pstryknięć wykonuje Pan(i) przypalając Malboro?"

    'style(
    '    Width = "3em";
    ')
    'codes(
    '{
    '    - "Nie wiem" DK,
    '    - "Te leki nie są dostępne na receptę" NA
    '}
    long;

    C2_3 "W jaki sposób przypala Pan(i) papierosy LM?"
    Categorical [1..1]
    {
        x1 "Zapałką",
        x2 "Zapalniczką",
        x3 "Od ogniska",
        x4 "Siłą woli",
        x5 "Inaczej, jak...?" other

    };

    C4_3 "Ile średnio licząc pstryknięć wykonuje Pan(i) przypalając LM?"

    'style(
    '    Width = "3em";
    ')
    'codes(
    '{
    '    - "Nie wiem" DK,
    '    - "Te leki nie są dostępne na receptę" NA
    '}
    long;

    C7 "Czy leki w różnych formach stosuje Pan(i)?"
    Categorical [1..1]
    {
        x1 "Zazwyczaj wszystkie naraz",
        x2 "Osobno - w zależności od objawów"

    };

```

<a name="for-categories"></a>
### FOR CATEGORIES

minijęzyk:
```
Q G Q1 COS
1 odp a
2 odp b
_
1 stw a {@}
2 stw b {@}

FOR CATEGORIES:
1 cat 1
2 cat 2

```
to_dim:

```

    Q1 - loop
    {
        c1 "cat 1",
        c2 "cat 2"

    } ran fields -
    (
        LR " COS" loop
        {
            l1 "stw a {@}",
            l2 "stw b {@}"

        } fields -
        (
            slice ""
            categorical [1..1]
            {
                x1 "odp a",
                x2 "odp b"

            };
        ) expand grid;
    ) expand;

```

<a name="prawa-strona"></a>
## Prawa strona
Abu uzyskać wejśćie do części web dodaj na początku linię
//to_web

```

    S1.Ask()
    if S1.ContainsAny("x1") then IOM.SbScreenOut()

    S5.Ask()

    if S5.ContainsAny("x1") then S6.Ask()

    C2_1.Ask()

    if C2_1.ContainsAny("x2") then C4_1.Ask()

    C2_2.Ask()

    if C2_2.ContainsAny("x2") then C4_2.Ask()

    C2_3.Ask()

    if C2_3.ContainsAny("x2") then C4_3.Ask()

```

<a name="precod-i-postcode"></a>
## precod i postcode
W części przypadkó IBISowy precod jest tłumaczony na język dimensions.
Czasem jednak chyba wygdniej byłoby podać taki prekod i postkod explicite.
Obecnie jest to rozwiązane w formie komentarza dimensions, czyli np <code>PRE ' xxx</code>

przykład:

```
//to_web
Q L Q1 cos
PRE ' xxx
POST ' yyy
```

wyjście:

```
    ' xxx
    Q1.Ask()
    ' yyy

```




<a name="python-recipes"></a>
# PYTHON RECIPES
<a name="json-to-dict-example"></a>
## json to dict example

```python
import json
from collections import OrderedDict

>>> # json - albo po prostu przerobiony fragment kwestionariusza
>>> text = """{"01":"7 sadów",
"02":"App!",
"03":"CiderINN",
"04":"Cydr Ignaców",
"05":"Cydr Lubelski",
"06":"Dobroński Cydr",
"07":"eXcite Strong Premium Cider",
"08":"Kiss",
"09":"Fizz",
"10":"Jocker",
"11":"Lajk",
"12":"My Cider",
"13":"Green Mill Cider",
"14":"Somersby",
"15":"Sun Cider",
"16":"Warka Cydr Premium",
"17":"XCider",
"18":"Cydr Polski",
"19":"Cydr Dziki",
"20":"Strongbow",
"21":"Cydr Miłosławski",
"22":"Cider Smiler",
"23":"Desire"}"""
>>>
>>> t = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(text)
>>> t
OrderedDict([('01', '7 sadów'), ('02', 'App!'), ('03', 'CiderINN'), ('04', 'Cydr Ignaców'), ('05', 'Cydr Lubelski'), ('06', 'Dobroński Cydr'), ('07', 'eXcite Strong Premium Cider'), ('08', 'Kiss'), ('09', 'Fizz'), ('10', 'Jocker'), ('11', 'Lajk'), ('12', 'My Cider'), ('13', 'Green Mill Cider'), ('14', 'Somersby'), ('15', 'Sun Cider'), ('16', 'Warka Cydr Premium'), ('17', 'XCider'), ('18', 'Cydr Polski'), ('19', 'Cydr Dziki'), ('20', 'Strongbow'), ('21', 'Cydr Miłosławski'), ('22', 'Cider Smiler'), ('23', 'Desire')])

```

<a name="english"></a>
# English


<a name="base-concepts"></a>
# Base Concepts

The base concept which is behind this soft is to safely automattion of processing the questionnaire to script.
I assumed that it will be difficult to enforce a particular shape of questionnaire. One of them will be in doc, others in xls, sometimes odf, pdf, other text format. Some will contain complex formatting, others do not.

I came to the conclusion that formatting should be done by scripter.

This process must be on the one hand as simple as possible, intuitive. On the other hand, there must be possible to enter as much information as possible.

How it looks now?
0. After receiving the questionnaire, I try to replace editor formatting to html formatting (bold, italics). In word i have a special macro for this.
1. Copying text to the editor - for example Notepad ++, sublime, or another text editor
2. Start the reformatting. Usually it means that I add a question type, some special markers. Set answerws cafeteria before statements cafeteria and separate them with _, add precode, postcode.
3. Paste this input into webapp, choose type of output and get it. 
4. Paste it to the mdd metadata or routing


<a name="why-webapp"></a>
### Why WebApp? 


I think it is maybe not the best way. But for sure it is simplest.
Go to the web page, paste input, get result.
You do not need to install anything, etc.

WebApp is not only one way that SDL can be used.

<a name="case-study"></a>
# Case study.

Recently I received survey where some parts were in word documents, and other parts (long lists i.e.) in excel.
Here is how I can handle something similar with it using SDL.

DOC content:

  Q1. What is Yours favorite car brand
  [Scripter: single answer, list in columns, sort it alphabeticaly]
  1 ALFA ROMEO
  ...
  69  SSANGYONG
  70  DODGE
  71  BUGATTI
  72  ACURA
    98. No one  [screenout]
  
    Q2 Which models of [brand] are the best
  [Scrpiter: list of models in excel files – sort it alpabetically, ask only for brand from Q1]

  Q3 Which car brand you never would have bought 
  [Scripter: list from Q1]


DOC after doc makro:

  Q1. What is Yours <b>favorite car brand</b>
  [Scripter: single answer, list in columns, sort it alphabeticaly]
  1 ALFA ROMEO
  2 AUDI
  ...
  69  SSANGYONG
  70  DODGE
  71  BUGATTI 
  72  ACURA
  98. No one  [screenout]
  Q2 Which models of <b>[brand]</b> are the best
  [Scrpiter: list of models in excel files – sort it alpabetically]

  Q3 Which car <b>brand</b> you <b>never would have bought</b> 
  [Scripter: list from Q1]


and here we have SDL input
I think - for now it's one of the most advanced examples, because there is a concept of nesting Python scripts.

  Q S Q1 What is Yours <b>favorite car brand</b> --sort --list:carBrands
  1    ALFA ROMEO
  ...
  69    SSANGYONG
  70    DODGE
  71    BUGATTI
  72    ACURA

  BEGIN PROGRAM
  import csv
  from collections import OrderedDict

  container = OrderedDict()

  # just copy this from excel,
  car_models = """brand    brand_id    model    model_id
  ALFA ROMEO    1    no model    0
  ALFA ROMEO    1    inne modele    1
  ...
  DODGE    70    CALIBER    31
  BUGATTI    71    no model    0
  ACURA    72    no model    0
  """

  def q2_questions(car_models):

      out = ""
      listy_marek = OrderedDict()

      models = csv.DictReader(car_models, delimiter="\t")
      
      for m in models:
          if m["brand_id"] in listy_marek.keys():
              listy_marek[m["brand_id"]].append(m["model_id"], m["model"]])
          else:
              listy_marek[m["brand_id"]] = []
              listy_marek[m["brand_id"]].append(m["model_id"], m["model"]])

      for key in listy_marek.keys():
          out += """
  Q M Q2_{0} Which models of <b>[brand]</b> are the best
  PRE 'if A3.ContainsAny("_{0}") then A4_{0}.Ask()
  """.format(key)
          listy = sorted(listy_marek[key], key=lambda x: x[1] )
          for el in listy:
              out += """0] + " " + el[1]            
  96.c Other... 
  97.d Don't know
  """.format(el[0], el[1])

  xxx = q1_questions(car_models)  # function call 

  END PROGRAM

  Q3 Which car <b>brand</b> you <b>never would have bought</b> 
  --use: carBrands


metadata output:

    carBrands - define
    {
        _72 "ACURA",
        _1 "ALFA ROMEO",
        _38 "ARO",
        ...
        _57 "WOŁGA",
        _58 "YUGO",
        _59 "ZAPOROŻEC",
        _60 "ŻUK"

    };

    Q1 "What is Yours <b>favorite car brand</b>   "
    Categorical [1..1]
    {
        use carBrands -
    };

    Q2_1 "Which models of <b>ALFA ROMEO</b> are the best"
    Categorical [1..]
    {
        _32 "145",
        _41 "146",
        _44 "147",
        _42 "155",
        _43 "156",
        _45 "159",
        _51 "164",
        _52 "166",
        _31 "33",
        _75 "4C",
        _20 "70",
        _74 "BRERA",
        _73 "GT",
        _72 "GTV",
        _33 "GULIETTA",
        _21 "MITO",
        _71 "SPIDER",
        _1 "inne modele",
        _0 "no model",
        _96 "Other..." other,
        - "Don't know" DK

    };

    Q2_2 "Which models of <b>AUDI</b> are the best"
    Categorical [1..]
    {
        _52 "100/100 QUATTRO",
        _62 "200/200 QUATTRO",
        _42 "80",
        _44 "80/90 QUATTRO",
        _43 "90",
        _21 "A1",
        _32 "A2",
        _31 "A3",
        _41 "A4/S4",
        _54 "A5/S5",
        _51 "A6/S6",
        _55 "A7",
        _61 "A8/S8",
        _53 "ALLROAD",
        _91 "Q3",
        _92 "Q5",
        _93 "Q7",
        _72 "R8",
        _71 "TT",
        _1 "inne modele",
        _0 "no model",
        _96 "Other..." other,
        - "Don't know" DK

    };

    ...

    Q2_69 "Which models of <b>SSANGYONG</b> are the best"
    Categorical [1..]
    {
        _93 "ACTYON",
        _94 "ACTYON SPORT",
        _95 "CORANDO",
        _92 "KORON",
        _91 "REXTON",
        _81 "RODIUS",
        _1 "inne modele",
        _0 "no model",
        _96 "Other..." other,
        - "Don't know" DK

    };

    Q2_70 "Which models of <b>DODGE</b> are the best"
    Categorical [1..]
    {
        _31 "CALIBER",
        _96 "Other..." other,
        - "Don't know" DK

    };

    Q2_71 "Which models of <b>BUGATTI</b> are the best"
    Categorical [1..]
    {
        _0 "no model",
        _96 "Other..." other,
        - "Don't know" DK

    };

    Q2_72 "Which models of <b>ACURA</b> are the best"
    Categorical [1..]
    {
        _0 "no model",
        _96 "Other..." other,
        - "Don't know" DK

    };

    Q3 "Which car <b>brand</b> you <b>never would have bought</b>"
    Categorical [1..]
    {
        use  carBrands -

    };

And web routing out - of course there is a bug - because filter is commented and there
shouldn't be asks outside. 
Web routing part is usually shorter. And here we have some logic to script. 
I think its better to prepare only a scratch of this part
web routing out

    Q1.Ask()

    'if A3.ContainsAny("_1") then A4_1.Ask()
    Q2_1.Ask()
    'if A3.ContainsAny("_2") then A4_2.Ask()
    Q2_2.Ask()
    'if A3.ContainsAny("_3") then A4_3.Ask()
    Q2_3.Ask()
    ...
    'if A3.ContainsAny("_70") then A4_70.Ask()
    Q2_70.Ask()
    'if A3.ContainsAny("_71") then A4_71.Ask()
    Q2_71.Ask()
    'if A3.ContainsAny("_72") then A4_72.Ask()
    Q2_72.Ask()
    Q3.Ask()



<a name="rules"></a>
# Rules: 
There are few simple rules to remember. 

I. When You create question syntax is almost always build like this:

  1 2     3   4                                     5
  Q QTYPE QID Question content (for now it should be at one line. Html is allowed.) --special_markers
    Cafeteria  (6)    
    _          (7)  
    Statements (8)

  1: Q - this mean that there will be a question definition. In other systems there can be also B for block, P for page.
  2: QTYPE - S|M|L|N|O|LHS|B|SDG|T|G|SLIDER|SLIDERS|H|R|CS|DEF
         S - Single
         M - Multi
         L - Page without form - just a text information
         N - Numeric
         O - Open (Text)
         LHS - love hate scale
         B - Baskets
         SDG - Simple Dynamic Grid
         T - Table
         G - Grid
         SLIDER
         SLIDERS
         H - Highlighter
         R - Rank
         CS - Concept select
         DEF - list definition
  
    3: QID - just an ID of question
  
    4: Content
  
    5: Special markers:
        
        --multi                 : multianswer in grids, tables
        --images                : image cafeteria
        --listcolumn            : cafeteria in columns
        --dezaktywacja          :
        --minchoose:x           : multi min choose
        --maxchoose:x           : multi max choose
        --nr                    : not require
    --int-implicite     : don't use first digit as a id (see [example]())
    --big-letters
    --lz:numbers      : add lead zeros to id
    --rot                   : cafeteria rotation   
        --ran                   : cafeteria random 
        --statements-rot        : statements rotation
        --statements-ran        : statements random

    IBIS
        --custom_css            : add custom css to page

        Dimensions
        --list:name             : define and use cafeteria object
        --use:name              : use cafeteria object

    (6) - cafeteria - (for some questions are obligatory)
    (7) - statements separator "_" - single underscore in line
    (8) - statements

    if you have 6 and 8 then (7) is obligatory



<a name="ibm-base-proffesional-examples"></a>
# IBM Base Proffesional examples

<a name="basic-question-types-and-definitions"></a>
## Basic question types and definitions


<a name="info-page"></a>
### Info page

input:

    Q L Q1_intro This is a message.

metadata output:

    Q1_intro "This is a message." info;

routing output:
    
    Q1_intro.Ask()

<a name="open-question"></a>
### Open question

input:

    Q O Q1_open This is open question.

metadata output:

    Q1_open "This is open question." text;

routing output:
    
    Q1_open.Ask()

<a name="numeric-question"></a>
### Numeric question

input:

    Q O Q1_numeric This is numeric question.

metadata output:

    Q1_numeric "This is numeric question."
    ' style( Width = "3em" )
    long;    

routing output:
    
    Q1_numeric.Ask()



<a name="simple-list-definition"></a>
### Simple list definition
Here is how a list can be defined explicite.
It's possible to define a list implicite, i.e. when a categorical question is created

Explicite

input:

  Q DEF Brands Smth
  2 a
  5 b
  7 c 

"Smth" it's artefact. It's possible to fix this in future iterations.

metadata output:

    Brands - define
    {
        _2 "a",
        _5 "b",
        _7 "c"

    };

routing output:
  
  None


<a name="categorical-single-answer"></a>
### Categorical single answer
Here is how a list can be defined explicite.
It's possible to define a list implicite, i.e. when a categorical question is created

Explicite

input:

    Q S Brands Smth
    2   a
    5   b
    7   c   

"Smth" it's artefact. It's possible to fix this in future iterations.

metadata output:

    Brands "Smth"
    Categorical [1..1]
    {
        _2 "a",
        _5 "b",
        _7 "c"

    };

routing output:
    
    Brands.Ask()

<a name="categorical-multiple-answer"></a>
### Categorical multiple answer
Here is how a list can be defined explicite.
It's possible to define a list implicite, i.e. when a categorical question is created

Explicite

input:

    Q M Brands Smth
    2   a
    5   b
    7   c   

"Smth" it's artefact. It's possible to fix this in future iterations.

metadata output:

    Brands "Smth"
    Categorical [1..1]
    {
        _2 "a",
        _5 "b",
        _7 "c"

    };

routing output:
    
    Brands.Ask()

<a name="categorical-with-defined-list"></a>
### Categorical with defined list

input:

    Q M Q1 which of the following brands you know
    --use:BRANDS

metadata output:

    Q1 "Which of the following brands you know?"
    Categorical [1..]
    {
        use BRANDS -

    };

routing output:
    
    Q1.Ask()

<a name="categorical-create-list"></a>
### Categorical create list

input:

    Q S Q1 The best car brand is .. --list:CARBRANDS
    Mercedes
    Bugatti
    Porsche


metadata output:

    CARBRANDS - define
    {
        _1 "Mercedes",
        _2 "Bugatti",
        _3 "Porsche"

    };

    Q1 "The best car brand is .. "
    Categorical [1..1]
    {
        use CARBRANDS -
    };

routing output:
    
    Q1.Ask()



<a name="automate-cafeteria-id"></a>
### Automate cafeteria id
There are several ways to automate cafeteria id's.

By default we expect that cafeteria has a numeric id, or no id at all.

cafeteria row is build like this:

    1   2         3        4  
    (id)(.d|.c)[ ]Content[](special markers) 

Groups in () are not obligatory
    
    1 - explicite id - natural numbers
    2 - .d - DK
        .c - comment (others)
    [ ] - white space: spaces, tabs
    3 - content 
    4 - special markers:
        --so = screen out (add screenout to routing)
        --fix
<a name="examples"></a>
#### Examples

<a name="basic-usage"></a>
##### Basic usage:
input:

    Q S Q1 Content
    1 A
    2 B
    3 C

output:

    Q1 "Content"
    Categorical [1..1]
    {
        _1 "A",
        _2 "B",
        _3 "C"

    };


input:

    Q S Q1 Content
    A
    B
    C

output:

    Q1 "Content"
    Categorical [1..1]
    {
        _1 "A",
        _2 "B",
        _3 "C"

    };

<a name="do-it-alphabetically---with-big-letters"></a>
##### do it alphabetically - with big letters

We can force big letters instead of numbers:

input:

    Q DEF LIST smth --big-letters
    el 1
    el 2

output:

    LIST - define
    {
        A "el 1",
        B "el 2"

    };

TODO: Exceeding the length of the alphabet. AA AB AC etc etc... Also Warning?

<a name="--raw-id"></a>
##### `--raw-id`

Other way is with `--raw-id`. Id is based on content. Replace white space with _ and strip.

input:

    Q M Q1 COS --raw-id
    Mark 1
    Mark 2
    Mark 3

output:

    Q1 "COS "
    Categorical [1..]
    {
        Mark_1 "Mark 1",
        Mark_2 "Mark 2",
        Mark_3 "Mark 3"

    };

<a name="--first-id"></a>
##### `--first-id`

For now the last method is `--first-id`. This means - first word treat like id.

input:

    Q M Q1 COS --first-id
    Argh Mark 1
    C Mark 2
    F Mark 3

output:

    Q1 "COS "
    Categorical [1..]
    {
        Argh "Mark 1",
        C "Mark 2",
        F "Mark 3"

    };


<a name="easy-add-bold-and-italic"></a>
##### Easy add bold and italic
When someone ask you to add a bold or italic to some answers, you don't need to add `<a></a>` arround phrase. Just add `--i`, `--b`.


input:
    
    Q S Q1 Smth
    A --i
    B --b
    C

output:

    Q1 "Smth"
    Categorical [1..1]
    {
        _1 "<i>A</i>",
        _2 "<b>B</b>",
        _3 "C"

    };


<a name="ref-na-dk"></a>
##### REF NA DK

input:
    
    Q S Q1 Smth
    A --ref
    B --na
    C --dk

output:

    Q1 "Smth"
    Categorical [1..1]
    {
        - "A" REF,
        - "B" NA,
        - "C" DK

    };

<a name="cafeteria-with-images"></a>
##### cafeteria with images
There are two ways to create cafeteria with images. 
You can use special marker `--images` or `--images:path\to\files` to do it globally (example 1a / 1b)
Or You can do it explicite with `|path\img.jpg` (example2)

example 1a
input:
    
    Q S Q1 Smth --images
    A
    B

output:

    Q1 "Smth "
        [
            flametatype = "mbclickableimages"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"

        ]
    Categorical [1..1]
    {
        _1 "A"
            labelstyle(
                Image = "images\1.jpg",
                ImagePosition = "ImageOnly"
            ),
        _2 "B"
            labelstyle(
                Image = "images\2.jpg",
                ImagePosition = "ImageOnly"
            )

    };

ecample 1b
input:
    
    Q DEF Q1 Smth --images:folder\folder2
    A
    B

output:

    Q1 - define
    {
        _1 "A"
            labelstyle(
                Image = "images\folder\folder2\1.jpg",
                ImagePosition = "ImageOnly"
            ),
        _2 "B"
            labelstyle(
                Image = "images\folder\folder2\2.jpg",
                ImagePosition = "ImageOnly"
            )

    };
'''

example 2:
input:
    
    Q S Q1 COS
    A|1.jpg
    B|c\2.jpg

output:

    Q1 "COS"
    Categorical [1..1]
    {
        _1 "A"
            labelstyle(
                Image = "images\1.jpg",
                ImagePosition = "ImageOnly"
            ),
        _2 "B"
            labelstyle(
                Image = "images\c\2.jpg",
                ImagePosition = "ImageOnly"
            )

    };

<a name="sorting"></a>
#### Sorting

Cafeteria have to methods to sort `--sort` and `--sort-by-id`

Example1 `--sort`
input:

    Q DEF Brand Brand --sort
    C
    D
    A

output:

    Brand - define
    {
        _3 "A",
        _1 "C",
        _2 "D"

    };


Example2  `--sort-by-id`
input:

    Q S Brand Brand --sort-by-id
    2 C
    3 D
    1 A

output:

    Brand "Brand "
    Categorical [1..1]
    {
        _1 "A",
        _2 "C",
        _3 "D"

    };

Example3 - You can combine sorting with list creation

input:

    Q M Brand Brand --sort--list:Brands
    C
    D
    A

output:

    Brands - define
    {
        _3 "A",
        _1 "C",
        _2 "D"

    };

    Brand "Brand "
    Categorical [1..]
    {
        use Brands -
    };



<a name="randomizerotation"></a>
#### Randomize/Rotation
To rotate/randomize add special marker

`--rot` - rotate cafeteria
`--statements-rot` - rotate statements

`--ran` - randomize cafeteria
`--statements-ran` - randomize statements

input:
    
    Q S Q1 COS --ran
    A
    B
    C


output:

    Q1 "COS"
    Categorical [1..1]
    {
        _1 "A",
        _2 "B",
        _3 "C"

    } ran ;

<a name="another-question-examples"></a>
## Another question examples

<a name="drag-and-drop"></a>
### Drag and Drop

<a name="buckets-with-text"></a>
#### Buckets with text

input:

    Q B dndBucketsText How familiar you are with each of these brands?<br/>
    --use:BE2A_ans_dl
    _
    --use:BRANDS

output:

    dndBucketsText "How familiar you are with each of these brands?<br/>"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "Text"
            ' , rowBtnWidth = 200                 ' width should be any integer > 10
            , dropType = "buckets"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use BE2A_ans_dl -

        };
    ) expand grid;


<a name="buckets-with-images"></a>
#### Buckets with images

input:

    Q B dndBucketsImage How familiar you are with each of these brands?<br/> --images
    --use:BE2A_ans_dl
    _
    --use:BRANDS

output:

    dndBucketsImage "How familiar you are with each of these brands?<br/>"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "Images"
            ' , rowBtnUseZoom = True             ' Setting to true enables a zoom icon on each of the row images that allows the respondents to view a larger version on screen.
            , dropType = "buckets"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            use BE2A_ans_dl -

        };
    ) expand grid;

<a name="exclude-in-buckets"></a>
#### Exclude in buckets

input:

    Q B dndScaleTextGray Drop the brand to the relevant baskets<br/>
    The Best one --@
    Good
    Bad
    The worse one --@
    _
    --use:BRANDS

output:

    dndScaleTextGray "Drop the brand to the relevant baskets<br/>"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "Text"
            ' , rowBtnWidth = 200                 ' width should be any integer > 10
            , dropType = "buckets"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            _1@ "The Best one",
            _2 "Good",
            _3 "Bad",
            _4@ "The worse one"

        };
    ) expand grid;



<a name="love-hate-scale-with-text-buttons"></a>
#### Love hate scale with text buttons

input:

    Q LHS dndLoveHateScaleText How familiar you are with each og these brands?<br/>
    -5 Hate it
    -4
    -3
    -2
    -1
    0 Neutral
    1
    2
    3
    4
    5 Love it
     _
     --use:BRANDS

output:

    dndLoveHateScaleText "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "Text"
            ' , rowBtnWidth = 200                 ' width should be any integer > 10
            , colImgType = "LoveHate"            ' RedBlack, Grey"
            , dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            _1 "-5 Hate it",
            _2 "-4",
            _3 "-3",
            _4 "-2",
            _5 "-1",
            _6 "0 Neutral",
            _7 "1",
            _8 "2",
            _9 "3",
            _10 "4",
            _11 "5 Love it"

        };
    ) expand grid;


<a name="love-hate-scale-with-image-buttons"></a>
#### Love hate scale with image buttons

it's similar - just add `--images`

input:

    Q LHS dndBucketsImage How familiar you are with each og these brands?<br/>--images
    -5 Hate it
    -4
    -3
    -2
    -1
    0 Neutral
    1
    2
    3
    4
    5 Love it
    _
    --use:BRANDS

output:

    dndBucketsImage "How familiar you are with each og these brands?<br/>"
        [
            flametatype = "mbdragndrop"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
            , rowBtnType = "Image"
            ' , rowBtnUseZoom = True             ' Setting to true enables a zoom icon on each of the row images that allows the respondents to view a larger version on screen.
            , colImgType = "LoveHate"            ' RedBlack, Grey"
            , dropType = "scale"
        ]
    loop
    {
        use BRANDS -

    }  fields -
    (
        slice ""
        categorical [1..]
        {
            _1 "-5 Hate it",
            _2 "-4",
            _3 "-3",
            _4 "-2",
            _5 "-1",
            _6 "0 Neutral",
            _7 "1",
            _8 "2",
            _9 "3",
            _10 "4",
            _11 "5 Love it"

        };
    ) expand grid;


<a name="dynamic-grid"></a>
#### Dynamic Grid

example 1
input:

    Q G Q1 COS
    answer a
    answer b
    _
    statment I
    statment II

output:

    Q1 "COS"
        [
            flametatype = "mbdynamicgrid"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        ]
    loop
    {
        _1 "statment I",
        _2 "statment II"

    } fields -
    (
        slice ""
        categorical [1..1]
        {
            _1 "answer a",
            _2 "answer b"

        };
    ) expand grid;

example2 - randomize cafeteria rotate statements

input:
    
    Q G Q1 COS --ran --statements-rot
    answer a
    answer b
    _
    statment I
    statment II

output:

    Q1 "COS "
        [
            flametatype = "mbdynamicgrid"
            , toolPath = "[%ImageCacheBase%]/images/mbtools/"
        ]
    loop
    {
        _1 "statment I",
        _2 "statment II"

    } rot  fields -
    (
        slice ""
        categorical [1..1]
        {
            _1 "answer a",
            _2 "answer b"

        } ran ;
    ) expand grid;

<a name="slider-not-implemented-yet"></a>
#### Slider (Not implemented yet)
Not implemented yet

<a name="click-and-fly-not-implemented-yet"></a>
#### Click and Fly (Not implemented yet)
Not implemented yest

<a name="clicakble-images"></a>
#### Clicakble Images 
Check single/multi with `--images`

<a name="clickable-tiles-not-implemented-yet"></a>
#### Clickable Tiles (Not implemented yet)
Not implemented yet

<a name="button-matrix-not-implemented-yet"></a>
#### Button Matrix (Not implemented yet)
Not implemented yet

<a name="semantic-differential-bi-polar---not-implemented-yet"></a>
#### Semantic Differential (Bi-polar) - Not implemented yet
Not implemented yet

<a name="errors-and-validation"></a>
# errors and validation
There are also few basic validators

<a name="two-questions-with-the-same-id"></a>
## two questions with the same id

input:

    Q S Q1 Smth
    A
    B

    Q S Q1 Smth
    A
    B


output:

    ValueError: Two questions have the same id: Q1  


<a name="two-positions-in-cafetera-have-the-same-id"></a>
## two positions in cafetera have the same id

input:

    Q S Q1 Smth
    1    A
    1    A

output:

    ValueError: Two positions can't have same id. Error in: Q1. Cafeteria id: 1   