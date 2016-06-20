| Title    | Survey Domain Language Examples          |
|----------|------------------------------------------|
| Author   | Rafał Korzeniewski                       |
| email    | korzeniewski@gmail.com                   |
| web      | http://rkorzen.pythonanywhere.com/parser |
| Date:    | Jun 20, 2016                             | 
| Version  | 0.01                                     |


# Change Log

| Data       | Version | Description                                       | Author             |
|------------|---------|---------------------------------------------------|--------------------|
| 20.06.2016 | 1.00    | Create Document                                   | Rafał Korzeniewski |

Survey Parser
-------------

# INDEX
<!-- MarkdownTOC autolink=true autoanchor=true bracket=round depth=5 -->

- [Base Concepts](#base-concepts)
	- [Why WebApp?](#why-webapp)
- [Case study.](#case-study)
- [Pressuppositons:](#pressuppositons)
- [IBM Base Proffesional examples](#ibm-base-proffesional-examples)
	- [Basic question types and definitions](#basic-question-types-and-definitions)
		- [Simple list definition](#simple-list-definition)

<!-- /MarkdownTOC -->


<a name="base-concepts"></a>
# Base Concepts

The base concept which is behind this soft is to safely automattion of processing the questionnaire to script.
I assumed that it will be difficult to enforce a particular shape of questionnaire. One of them will be in doc, others in xls, sometimes odf, pdf, other text format. Some will contain complex formatting, others do not.

I came to the conclusion that formatting should be done by scripter.Doszedłem do wniosku

This process must be on the one hand as simple as possible. On the other hand, there must be possible to enter as much information as possible.

How it looks now?
0. After receiving the questionnaire, I try to replace editor formatting to html formatting (bold, italics). In word i have a special macro for this.

1. Copying text to the editor - for example Notepad ++, sublime, or another text editor
2. Start to reformatting. Usually it means that I add a question type, some special markers. Set answerws cafeteria before statements cafeteria and separate them, add precode, postcode.
3. Paste this input into webapp choose type of output and get it. 
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
	1	ALFA ROMEO
	...
	69	SSANGYONG
	70	DODGE
	71	BUGATTI
	72	ACURA
	             98. No one  [screenout]
	Q2 Which models of [brand] are the best
	[Scrpiter: list of models in excel files – sort it alpabetically, ask only for brand from Q1]

	Q3 Which car brand you never would have bought 
	[Scripter: list from Q1]


DOC after doc makro:

	Q1. What is Yours <b>favorite car brand</b>
	[Scripter: single answer, list in columns, sort it alphabeticaly]
	1	ALFA ROMEO
	2	AUDI
	...
	69	SSANGYONG
	70	DODGE
	71	BUGATTI	
	72	ACURA
	98. No one  [screenout]
	Q2 Which models of <b>[brand]</b> are the best
	[Scrpiter: list of models in excel files – sort it alpabetically]

	Q3 Which car <b>brand</b> you <b>never would have bought</b> 
	[Scripter: list from Q1]


and here we have SDL input
I think - for now it's one of the most advanced examples, because there is a concept of nesting Python scripts.

	Q S Q1 What is Yours <b>favorite car brand</b> --sort --list:carBrands --listcolumn:3 
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



<a name="pressuppositons"></a>
# Pressuppositons: 
There are few simple rules to remember. 

I. When You create question syntax is always build like this:

	1 2     3   4																      5
	Q QTYPE QID Question content (for now it should be at one line. Html is allowed.) --special_markers

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
		--int-implicite			: don't use first digit as a id (see [example]())
		--big-letters
		--lz:numbers			: add lead zeros to id
		
		IBIS
        --custom_css            : add custom css to page

        Dimensions
        --list:name             : define and use cafeteria object
        --use:name              : use cafeteria object


<a name="ibm-base-proffesional-examples"></a>
# IBM Base Proffesional examples

<a name="basic-question-types-and-definitions"></a>
## Basic question types and definitions

<a name=""></a>
<a name="simple-list-definition"></a>
### Simple list definition
Here is how a list can be defined explicite.
It's possible to define a list implicite, i.e. when a categorical question is created

Explicite

input:

	Q DEF Brands Brands
	2	a
	5	b
	7	c	

double "Brands" it's artefact. It's possible to fix this in future iterations.

metadata output:

    Brands - define
    {
        _1 "a",
        _2 "b",
        _3 "c"

    };

routing output:
	
	None

