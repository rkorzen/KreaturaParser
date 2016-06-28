# -*- coding: UTF-8 -*-
import textwrap

__author__ = 'KorzeniewskiR'


def is_arithmetic(l):
    """Check if sequence is arithmetic or not

    :param l: list of int

    """

    if len(l) < 3:
        return False

    try:
        list(map(int, l))
    except ValueError:
        return False

    # delta = l[1] - l[0]  # in normal situation
    delta = 1  # for syntax purposes
    for index in range(len(l) - 1):
        if not (l[index + 1] - l[index] == delta):
            return False
    return True


def add_comment(text):
    """Spss comment syntax

    :param text: text of syntax

    """

    out = "/* " + "\n/* ".join(textwrap.wrap(text))

    return out + "\n"


def numeric(question, wd="F2.0"):
    """Create NUMERIC variables

    :returns String: spss syntax to create NUMERIC variables
    :param question: .elements.Question object
    :param wd: width and decimals. Default = F2.0 (float with 2 digits width and 0 decimals)

    Function olso try to wrap and format nice looking syntax
    """

    id_ = question.id
    items = question.cafeteria

    # begining
    out = "NUMERIC\n".format(type)

    m = [id_ + '_' + item.id for item in items]
    indexes = [int(item.id) for item in items]

    if is_arithmetic(indexes):
        item_list = " {} to {}".format(m[0], m[-1])
    else:
        item_list = " ".join(m)
        item_list = " " + "\n ".join(textwrap.wrap(item_list, 80))

    out += item_list
    out += " ({}).\nEXECUTE.\n".format(wd)
    return out


def recode(question, values="(else=99)"):
    """recode variables (NUMERIC)

    :returns String: spss syntax to recode NUMERIC variables
    :param question: .elements.Question object
    :param values: parameter for syntax recode. For example:
                   default: (else=99)
                   other: (1=-5)(2=-4)(3=-3)(4=-2)(5=-1)(6=0)(7=1)(8=2)(9=3)(10=4)(11=5)

    Function also try to wrap and format nice looking syntax
    """

    id_ = question.id
    items = question.cafeteria

    # begining
    out = "recode\n".format(type)

    m = [id_ + '_' + item.id for item in items]
    indexes = [int(item.id) for item in items]

    if is_arithmetic(indexes):
        item_list = " {} to {}".format(m[0], m[-1])
    else:
        item_list = " ".join(m)
        item_list = " " + "\n ".join(textwrap.wrap(item_list, 80))

    out += item_list
    out += " {}.\nEXECUTE.\n".format(values)
    return out


def do_repeat(question):
    """Returns syntax for main loop for recoding baskets (IBIS generatet) data from..

    :param id_: Question prefix
    :param n: number of baskets

    In repeat loop are:
    As many columns as baskets
    As many rows as things

    """

    id_ = question.id
    n = len(question.statements)
    things = question.cafeteria

    out = "DO REPEAT x=1 TO " + str(n)
    for t in things:
        out += " / X{0}x_{1}= ".format(id_, t.id)
        out += " ".join(["{0}x{2}_{1}".format(id_, t.id, j) for j in range(1, n+1)]) + "\n"

    out = out[:-1] + ".\n"
    for t in things:
        out += 'if (X{0}x_{1}=1) {0}_{1}=x.\n'.format(id_, t.id)
    out += "END REPEAT.\nEXECUTE.\n\n"

    return out


def var_lab(question, lista=None):

    id_ = question.id
    if lista:
        things = lista.cafeteria
    else:
        things = question.cafeteria
    statement = question.content

    out = ""
    for thing in things:
        for m in ["--dk", "--na", "--ref"]:
            if m in thing.content:
                thing.content = thing.content.replace(m, "")
        thing.content = thing.content.strip()
        out += 'var lab {0}_{1} "{0}_{1} | {2} | {3} ".\n'.format(id_, thing.id, thing.content, statement)

    return out


def val_lab(question):
    id_ = question.id
    items = question.cafeteria
    cafeteria = question.statements
    caf = ""
    for c in cafeteria:
        caf += " {} '{}'\n".format(c.id, c.content)

    m = [id_ + '_' + item.id for item in items]
    indexes = [int(item.id) for item in items]

    if is_arithmetic(indexes):
        item_list = " {} to {}".format(m[0], m[-1])
    else:
        item_list = " ".join(m)
        item_list = " " + "\n ".join(textwrap.wrap(item_list, 80))

    out = "val lab " + item_list + "\n" + caf + ".\n\n"
    return out


def baskets_syntax(question):
    id_ = question.id
    items = question.cafeteria
    statements = question.statements
    n_baskets = len(items)
    #marki = [[x.split(';')[0], x.split(';')[1]] for x in marki.splitlines()]

    out = add_comment("START {} baskets clean sytax".format(id_))
    out += numeric(question)
    out += recode(question)
    out += do_repeat(question)
    out += var_lab(question)
    out += val_lab(question)
    out += add_comment("END {} baskets clean sytax".format(id_))
    return out


def multi_syntax(question):
    id_ = question.id
    old, new = [], []

    for c, caf in enumerate(question.cafeteria):
        old.append(id_ + str(c+1))
        new.append(id_ + "_" + caf.id)

    old = " ".join(old)
    new = " ".join(new)

    rename_tmp = "RENAME VARIABLES ({} = {}).\nEXECUTE.\n"

    syntax = rename_tmp.format(old, new)

    return syntax




if __name__ == "__main__":
    from kparser import parse

    text = """

    Q B Q1 COS
    01 A
    02 B
    03 C
    04 D
    _
    1 0 never
    2 1
    3 2
    4 3
    5 4
    6 5
    7 6
    8 7
    9 8
    10 9
    11 10 always"""
    survey = parse(text)
    question = survey.childs[0].childs[0].childs[0]


    def test_single_n_is_arithmetic():
        assert is_arithmetic([0]) == False

    def test_arithmetic_non():
        x = ['a', 'b', 'c', 'd']
        assert is_arithmetic(x) == False

    def test_is_arithmetic():
        seq = [1, 2, 3, 4, 5, 6, 7, 8]
        assert is_arithmetic(seq) == True

    def test_is_not_arithmetic():
        seq = [1, 5, 3, 4, 5, 6, 7, 8]
        assert is_arithmetic(seq) == False

    def test_comment():
        print(add_comment("A"))
        assert add_comment("A") == "/* A\n"

    def test_comment_wrap():
        text = """Lorem ipsum dolor sit amet enim. Etiam ullamcorper. Suspendisse a pellentesque dui, non felis. Maecenas malesuada elit lectus felis, malesuada ultricies. Curabitur et ligula. Ut molestie a, ultricies porta urna. Vestibulum commodo volutpat a, convallis ac, laoreet enim. Phasellus fermentum in, dolor. Pellentesque facilisis. Nulla imperdiet sit amet magna. Vestibulum dapibus, mauris nec malesuada fames ac turpis velit, rhoncus eu, luctus et interdum adipiscing wisi. Aliquam erat ac ipsum. Integer aliquam purus. Quisque lorem tortor fringilla sed, vestibulum id, eleifend justo vel bibendum sapien massa ac turpis faucibus orci luctus non, consectetuer lobortis quis, varius in, purus. Integer ultrices posuere cubilia Curae, Nulla ipsum dolor lacus, suscipit adipiscing. Cum sociis natoque penatibus et ultrices volutpat. Nullam wisi ultricies a, gravida vitae, dapibus risus ante sodales lectus blandit eu, tempor diam pede cursus vitae, ultricies eu, faucibus quis, porttitor eros cursus lectus, pellentesque eget, bibendum a, gravida ullamcorper quam. Nullam viverra consectetuer. Quisque cursus et, porttitor risus. Aliquam sem. In hendrerit nulla quam nunc, accumsan congue. Lorem ipsum primis in nibh vel risus. Sed vel lectus. Ut sagittis, ipsum dolor quam."""

        assert add_comment(text) == """/* Lorem ipsum dolor sit amet enim. Etiam ullamcorper. Suspendisse a
/* pellentesque dui, non felis. Maecenas malesuada elit lectus felis,
/* malesuada ultricies. Curabitur et ligula. Ut molestie a, ultricies
/* porta urna. Vestibulum commodo volutpat a, convallis ac, laoreet enim.
/* Phasellus fermentum in, dolor. Pellentesque facilisis. Nulla imperdiet
/* sit amet magna. Vestibulum dapibus, mauris nec malesuada fames ac
/* turpis velit, rhoncus eu, luctus et interdum adipiscing wisi. Aliquam
/* erat ac ipsum. Integer aliquam purus. Quisque lorem tortor fringilla
/* sed, vestibulum id, eleifend justo vel bibendum sapien massa ac turpis
/* faucibus orci luctus non, consectetuer lobortis quis, varius in,
/* purus. Integer ultrices posuere cubilia Curae, Nulla ipsum dolor
/* lacus, suscipit adipiscing. Cum sociis natoque penatibus et ultrices
/* volutpat. Nullam wisi ultricies a, gravida vitae, dapibus risus ante
/* sodales lectus blandit eu, tempor diam pede cursus vitae, ultricies
/* eu, faucibus quis, porttitor eros cursus lectus, pellentesque eget,
/* bibendum a, gravida ullamcorper quam. Nullam viverra consectetuer.
/* Quisque cursus et, porttitor risus. Aliquam sem. In hendrerit nulla
/* quam nunc, accumsan congue. Lorem ipsum primis in nibh vel risus. Sed
/* vel lectus. Ut sagittis, ipsum dolor quam.
"""

    def test_numeric_one():
        text = """
Q B Q1 COS
01 A
_
1 A
2 B
"""
        survey = parse(text)
        question = survey.childs[0].childs[0].childs[0]
        print(numeric(question))
        assert numeric(question) == """NUMERIC
 Q1_01 (F2.0).
EXECUTE.
"""

    def test_numeric_wrapping():
        survey = parse("""Q B DLUGIEIDPYTANIA COS
01 A
02 B
03 C
04 D
05 E
06 F
07 G
08 H
09 I
10 J
11 K
12 L
13 M
14 N
15 O
16 P
17 Q
18 R
19 S
20 T
21 U
22 V
23 W
24 X
25 Y
27 Z
_
1 A
2 B
3 C""")
        question = survey.childs[0].childs[0].childs[0]
        print(numeric(question))
        assert numeric(question) == """NUMERIC
 DLUGIEIDPYTANIA_01 DLUGIEIDPYTANIA_02 DLUGIEIDPYTANIA_03 DLUGIEIDPYTANIA_04
 DLUGIEIDPYTANIA_05 DLUGIEIDPYTANIA_06 DLUGIEIDPYTANIA_07 DLUGIEIDPYTANIA_08
 DLUGIEIDPYTANIA_09 DLUGIEIDPYTANIA_10 DLUGIEIDPYTANIA_11 DLUGIEIDPYTANIA_12
 DLUGIEIDPYTANIA_13 DLUGIEIDPYTANIA_14 DLUGIEIDPYTANIA_15 DLUGIEIDPYTANIA_16
 DLUGIEIDPYTANIA_17 DLUGIEIDPYTANIA_18 DLUGIEIDPYTANIA_19 DLUGIEIDPYTANIA_20
 DLUGIEIDPYTANIA_21 DLUGIEIDPYTANIA_22 DLUGIEIDPYTANIA_23 DLUGIEIDPYTANIA_24
 DLUGIEIDPYTANIA_25 DLUGIEIDPYTANIA_27 (F2.0).
EXECUTE.
"""

    def test_numeric_range():
        print(numeric(question))
        assert numeric(question) == """NUMERIC
 Q1_01 to Q1_04 (F2.0).
EXECUTE.
"""

    def test_numeric_wd():
        print(numeric(question, "F3.1"))
        assert numeric(question, "F3.1") == """NUMERIC
 Q1_01 to Q1_04 (F3.1).
EXECUTE.
"""

    def test_recode():
        print(recode(question))
        assert recode(question) == """recode
 Q1_01 to Q1_04 (else=99).
EXECUTE.
"""

    def test_recode_values():
        val = "(1=-5)(2=-4)(3=-3)(4=-2)(5=-1)(6=0)(7=1)(8=2)(9=3)(10=4)(11=5)"
        print(recode(question, val))
        assert recode(question, val) == """recode
 Q1_01 to Q1_04 (1=-5)(2=-4)(3=-3)(4=-2)(5=-1)(6=0)(7=1)(8=2)(9=3)(10=4)(11=5).
EXECUTE.
"""

    def test_recode_wrapping():
        survey = parse("""Q B DLUGIEIDPYTANIA COS
        01 A
        02 B
        03 C
        04 D
        05 E
        06 F
        07 G
        08 H
        09 I
        10 J
        11 K
        12 L
        13 M
        14 N
        15 O
        16 P
        17 Q
        18 R
        19 S
        20 T
        21 U
        22 V
        23 W
        24 X
        25 Y
        27 Z
        _
        1 A
        2 B
        3 C""")
        question = survey.childs[0].childs[0].childs[0]
        print(recode(question))
        assert recode(question) == """recode
 DLUGIEIDPYTANIA_01 DLUGIEIDPYTANIA_02 DLUGIEIDPYTANIA_03 DLUGIEIDPYTANIA_04
 DLUGIEIDPYTANIA_05 DLUGIEIDPYTANIA_06 DLUGIEIDPYTANIA_07 DLUGIEIDPYTANIA_08
 DLUGIEIDPYTANIA_09 DLUGIEIDPYTANIA_10 DLUGIEIDPYTANIA_11 DLUGIEIDPYTANIA_12
 DLUGIEIDPYTANIA_13 DLUGIEIDPYTANIA_14 DLUGIEIDPYTANIA_15 DLUGIEIDPYTANIA_16
 DLUGIEIDPYTANIA_17 DLUGIEIDPYTANIA_18 DLUGIEIDPYTANIA_19 DLUGIEIDPYTANIA_20
 DLUGIEIDPYTANIA_21 DLUGIEIDPYTANIA_22 DLUGIEIDPYTANIA_23 DLUGIEIDPYTANIA_24
 DLUGIEIDPYTANIA_25 DLUGIEIDPYTANIA_27 (else=99).
EXECUTE.
"""

    def test_recode_lead_zero():
        x = [["01", "A"], ["02", "A"], ["03", "A"], ["04", "A"], ["05", "A"]]
        print(recode("A", x))
        assert recode("A", x) == """recode
 A_01 to A_05 (else=99).
EXECUTE.
"""

    def test_do_repeat():
        print(do_repeat(question))
        assert do_repeat(question) == """DO REPEAT x=1 TO 11 / XQ1x_01= Q1x1_01 Q1x2_01 Q1x3_01 Q1x4_01 Q1x5_01 Q1x6_01 Q1x7_01 Q1x8_01 Q1x9_01 Q1x10_01 Q1x11_01
 / XQ1x_02= Q1x1_02 Q1x2_02 Q1x3_02 Q1x4_02 Q1x5_02 Q1x6_02 Q1x7_02 Q1x8_02 Q1x9_02 Q1x10_02 Q1x11_02
 / XQ1x_03= Q1x1_03 Q1x2_03 Q1x3_03 Q1x4_03 Q1x5_03 Q1x6_03 Q1x7_03 Q1x8_03 Q1x9_03 Q1x10_03 Q1x11_03
 / XQ1x_04= Q1x1_04 Q1x2_04 Q1x3_04 Q1x4_04 Q1x5_04 Q1x6_04 Q1x7_04 Q1x8_04 Q1x9_04 Q1x10_04 Q1x11_04.
if (XQ1x_01=1) Q1_01=x.
if (XQ1x_02=1) Q1_02=x.
if (XQ1x_03=1) Q1_03=x.
if (XQ1x_04=1) Q1_04=x.
END REPEAT.
EXECUTE.

"""

    def test_var_lab():
        text = """

        Q B Q1 COS
        01 A
        02 B
        03 C
        04 D
        _
        1 Always
        2 Sometimes
        3 Never
"""
        survey = parse(text)
        question = survey.childs[0].childs[0].childs[0]
        print(var_lab(question))
        assert var_lab(question) == """var lab Q1_01 "Q1_01 | A | COS ".
var lab Q1_02 "Q1_02 | B | COS ".
var lab Q1_03 "Q1_03 | C | COS ".
var lab Q1_04 "Q1_04 | D | COS ".
"""

    def test_val_lab():
        text = """

                Q B Q1 COS
                01 A
                02 B
                03 C
                04 D
                _
                1 Always
                2 Sometimes
                3 Never
        """
        survey = parse(text)
        question = survey.childs[0].childs[0].childs[0]
        print(val_lab(question))
        assert val_lab(question) == """val lab  Q1_01 to Q1_04
 1 'Always'
 2 'Sometimes'
 3 'Never'
.

"""

    def test_baskets_syntax():
        print(baskets_syntax(question))
        assert baskets_syntax(question) == """/* START Q1 baskets clean sytax
NUMERIC
 Q1_01 to Q1_04 (F2.0).
EXECUTE.
recode
 Q1_01 to Q1_04 (else=99).
EXECUTE.
DO REPEAT x=1 TO 11 / XQ1x_01= Q1x1_01 Q1x2_01 Q1x3_01 Q1x4_01 Q1x5_01 Q1x6_01 Q1x7_01 Q1x8_01 Q1x9_01 Q1x10_01 Q1x11_01
 / XQ1x_02= Q1x1_02 Q1x2_02 Q1x3_02 Q1x4_02 Q1x5_02 Q1x6_02 Q1x7_02 Q1x8_02 Q1x9_02 Q1x10_02 Q1x11_02
 / XQ1x_03= Q1x1_03 Q1x2_03 Q1x3_03 Q1x4_03 Q1x5_03 Q1x6_03 Q1x7_03 Q1x8_03 Q1x9_03 Q1x10_03 Q1x11_03
 / XQ1x_04= Q1x1_04 Q1x2_04 Q1x3_04 Q1x4_04 Q1x5_04 Q1x6_04 Q1x7_04 Q1x8_04 Q1x9_04 Q1x10_04 Q1x11_04.
if (XQ1x_01=1) Q1_01=x.
if (XQ1x_02=1) Q1_02=x.
if (XQ1x_03=1) Q1_03=x.
if (XQ1x_04=1) Q1_04=x.
END REPEAT.
EXECUTE.

var lab Q1_01 "Q1_01 | A | COS ".
var lab Q1_02 "Q1_02 | B | COS ".
var lab Q1_03 "Q1_03 | C | COS ".
var lab Q1_04 "Q1_04 | D | COS ".
val lab  Q1_01 to Q1_04
 1 '0 never'
 2 '1'
 3 '2'
 4 '3'
 5 '4'
 6 '5'
 7 '6'
 8 '7'
 9 '8'
 10 '9'
 11 '10 always'
.

/* END Q1 baskets clean sytax
"""

    test_single_n_is_arithmetic()
    test_arithmetic_non()
    test_is_arithmetic()
    test_is_not_arithmetic()
    test_comment()
    test_comment_wrap()
    test_numeric_one()
    test_numeric_wrapping()
    test_numeric_range()
    test_numeric_wd()
    test_recode()
    test_recode_values()
    test_recode_wrapping()
    test_do_repeat()
    test_var_lab()
    test_val_lab()
    test_baskets_syntax()

