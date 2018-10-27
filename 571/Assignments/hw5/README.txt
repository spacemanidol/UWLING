Daniel Campos
Ling 571 HW5
10/26/2018
FCFG 
1. Results
(ROOT[] (S[] (NP[NUM='pl'] (Det[] the) (N[NUM='pl'] dogs)) (VP[NUM='pl', TENSE='pres'] (AIV[NUM='pl', TENSE='pres'] bark))) (PUNC[] .))
(ROOT[] (S[] (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] dog)) (VP[NUM='sg', TENSE='pres'] (IV[NUM='sg', TENSE='pres'] barks) )) (PUNC[] .))



(ROOT[] (S[] (NP[NUM='pl'] (N[NUM='pl'] dogs)) (VP[NUM='pl', TENSE='pres'] (AIV[NUM='pl', TENSE='pres'] bark))) (PUNC[] .))

(ROOT[] (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[NUM=?n, TENSE='past'] (ATV[TENSE='past'] thought) (NP[NUM=?n] (PRONOUN[] that)) (S[] (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] book)) (VP[NUM=?n, TENSE='past'] (ATV[TENSE='past'] was) (ADJ[] interesting))))) (PUNC[] .))


(ROOT[] (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[NUM=?n, TENSE=?t] (ATV[TENSE='past'] put) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] book)) (PP1[] (PREP1[] on) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] shelf))))) (PUNC[] .))
(ROOT[] (S[]  (VP[NUM=?n, TENSE='past'] (TV[TENSE='past'] did) (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[NUM=?n, TENSE=?t] (ATV[TENSE='past'] put) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] book)) (PP1[] (PREP1[] on) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] shelf))))))) (PUNC[] ?))

(ROOT[] (S[] (NP[NUM=?n] (PRONOUN[] what)) (VP[NUM=?n, TENSE='past'] (TV[TENSE='past'] did) (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[NUM=?n, TENSE=?t] (ATV[TENSE='past'] put)  (PP1[] (PREP1[] on) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] shelf))))))) (PUNC[] ?))

(ROOT[] (S[] (NP[NUM=?n] (PRONOUN[] what)) (VP[NUM='sg', TENSE='pres'] (TV[NUM='sg', PERS='third', TENSE='pres'] does) (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[NUM='sg', TENSE='pres'] (IV[NUM='sg', TENSE='pres'] know) )))) (PUNC[] ?))
(ROOT[] (S[] (NP[NUM=?n] (PRONOUN[] what)) (VP[NUM='sg', TENSE='pres'] (TV[NUM='sg', PERS='third', TENSE='pres'] does) (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[NUM='sg', TENSE='pres'] (TV[NUM='sg', TENSE='pres'] think) (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[NUM='sg', TENSE='pres'] (IV[NUM='sg', TENSE='pres'] knows) )))))) (PUNC[] ?))
(ROOT[] (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[GEND='f', NUM=?n, TENSE='past'] (TV[TENSE='past'] saw) (NP[GEND='f', NUM='sg'] (ProfRef[GEND='f', NUM='sg'] herself)))) (PUNC[] .))

(ROOT[] (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[GEND='m', NUM=?n, TENSE='past'] (TV[TENSE='past'] saw) (NP[GEND='m', NUM='sg'] (ProfRef[GEND='m', NUM='sg'] himself)))) (PUNC[] .))
(ROOT[] (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[NUM=?n, TENSE='past'] (TV[TENSE='past'] reached) (NP[NUM='sg'] (Det[] the) (N[NUM='sg'] summit)) (PP1[] (PREP1[] on) (NP[NUM='sg'] (N[NUM='sg'] Tuesday))))) (PUNC[] .))

(ROOT[] (S[] (NP[GEND='m', NUM='sg'] (PropN[GEND='m', NUM='sg'] John)) (VP[NUM=?n, TENSE='past'] (IV[TENSE='past'] walked) (PP1[] (PREP1[] on) (NP[NUM='sg'] (N[NUM='sg'] Tuesday))))) (PUNC[] .))
(ROOT[] (S[] (NP[GEND='f', NUM='sg'] (PropN[GEND='f', NUM='sg'] Mary)) (VP[NUM=?n, TENSE='past'] (IV[TENSE='past'] walked) (PP2[] (PREP2[] for)  (NP[NUM='pl'] (Det[] five) (N[NUM='pl'] minutes))))) (PUNC[] .))
2. Approach & Work
a. fcfg grammar
    To solve this problem my approach was first let me create a program that accepts all the sentences that I need to accept and then modify my grammar to reject the sentences we were supposed to reject. 
    Initially that had me looking up all the words in parsers and dictionaries to find out their verb/noun type and then playing around to make my grammar clear and consise. Once I had that working well
    I created 2 test files, pass_sentences.txt and fail_sentences.txt and created a script that would run both and output all those that I was supposed to parse and fail and those I wasnt suppose to parse but did.
    From there I slowly started tweaking my grammar and adding more specific rules until I had a grammar that rejected everything it was supposed to and parsed everything it was. The funny thing is initially I didnt see that there was a sentences_key.txt file so I was trying to
    figure out if sentences were gramatically correct on my own at first and tuned my grammar towards my thoughts. I was quite surprised when I looked at the file and saw that many things I had deemed 'real' were not. Took me a while to tune my grammar to match its new goal.
b. NLTK Parser: 
    To implement this I mostly built off the code supplied in the ipython notebook and my hw1 until I had a parser that given could replicate the desired outputs with the example_sentence and example_grammar.fcfg.

3. Problems
   The only probem the system had is it was occasionally adding an extra NP[] but I found it easier just to remove that with python that debug my logic. Not perfect but it got the job done.

4. Insights
   This home work really taught me how hard it is to make a grammar. Starting from what would be considered a clean and consise grammar one has to add a bunch of one of rules and exceptions are everywhere.
   This really highlights to me why NLP is so hard. Unlike other sciences, languges does not tend to follow the same sets of rules all the time and it makes creating a good system quite difficult. 
   I cant imagine creating a hand crafted grammar at scale, it would be incredibly difficult and troublesome. 

   Some of the strings I really struggled with were all those involving put. Basically since when this verb was used, some types of following words were allowed but others were not. It made tuning the rules of the grammar tricky. 
   Mary put the book .
   Mary put the book on the shelf .
   did Mary put the book on the shelf ?
   put Mary the book on the shelf ?
   what did Mary put on the shelf ?
   what did Mary put ?