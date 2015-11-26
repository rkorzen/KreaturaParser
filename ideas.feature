# Created by KorzeniewskiR at 2015-11-26
Feature: Pętla w pętli #Enter feature name here
  # Enter feature description here
  Standardowo w pytaniach mamy kafeterię odp i stwierdzeń
  W ibisie to wystarcza, ale w dim można dodac jeszcze level wyżej - categorie
  W IBIS to załatwiane jest pętlą pythonową.
  W DIM trzeba to obsłużyć odpowiednią strukturą.

  Scenario: # Enter scenario name here
    # Enter steps here
    Q G Q1 COS
    1 odp a
    2 odp b
    _
    1 stw a [cat]
    2 stw b [cat]

    LOOP FOR CATEGORY:
    1 cat 1
    2 cat 2

    co przekładało by się na:

    DIM:
    Q1 - loop
    {
        c1 "cat 1",
        c2 "cat 2"
    } ran fields -
    (
        LR " COS" loop
        {
            l1 "stw a {@} ",
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

    IBIS:

    Q G Q1_1 COS
    1 odp a
    2 odp b
    _
    1 stw a cat 1
    2 stw b cat 1

    Q G Q1_2 COS
    1 odp a
    2 odp b
    _
    1 stw a cat 2
    2 stw b cat 2