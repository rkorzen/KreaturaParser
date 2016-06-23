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


<a name="base-concepts"></a>
# Base Concepts

The base concept which is behind this soft is to safely automattion of processing the questionnaire to script.
I assumed that it will be difficult to enforce a particular shape of questionnaire. One of them will be in doc, others in xls, sometimes odf, pdf, other text format. Some will contain complex formatting, others do not.

I came to the conclusion that formatting should be done by scripter.Doszedłem do wniosku

This process must be on the one hand as simple as possible. On the other hand, there must be possible to enter as much information as possible.

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



<a name="rules"></a>
# Rules: 
There are few simple rules to remember. 

I. When You create question syntax is almost always build like this:

	1 2     3   4																      5
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
		--int-implicite			: don't use first digit as a id (see [example]())
		--big-letters
		--lz:numbers			: add lead zeros to id
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
	2	a
	5	b
	7	c	

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