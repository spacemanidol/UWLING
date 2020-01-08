Daniel Campos
Ling 571 HW3
10/12/2018
CKY Parser
1. Results(Examples)
      (VBN discovered)
      (SBAR
        (_X_2 that)
        (S
          (NP malaria)
          (_X_5
            (VP
              (VBZ invades)
              (NP (Det the) (Nom (ADJP whole) (Nom body))))
            (PUNC .)))))))
(TOP
  (NP Scientists)
  (_X_6
    (VP
      (AUX have)
      (VP
        (VBN discovered)
        (SBAR
          (_X_2 that)
          (S
            (NP malaria)
            (VP
              (VBZ invades)
              (NP (Det the) (Nom (ADJP whole) (Nom body))))))))
    (PUNC .)))
Number of parses: 2
2. Approach
Given the amount of pseudo code online and in class the implementation for this assignment was much more straight forward. First, I took in the grammar file and read it, next I opened my sentences file and line by line tokenized and then pass the grammar and the tokenized input to my cky algorith. 
My cky algorithm is just a simple implementation of what is described in the slides along with a back pointer table as discussed in class. When the algortihm finishes, we take the [0][n] list in the back pointer table and then parse it. To parse it I decided to use recusion to create NLTK.Trees since it seemed like the easiest way to debug my progress and to make the code expandable for futrue use.
3. Problems 
No problems after I created my own node class. At first I spent a long time trying to use Tuples instead but it made navigating, debuging and printing very very difficult.