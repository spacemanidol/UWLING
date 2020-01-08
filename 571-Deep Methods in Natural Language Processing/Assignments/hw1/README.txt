Daniel Campos
Ling 571 HW1
09/28/2018
1. Results(Example)
the cat chased the dog
(S (NP (Det the) (N cat)) (VP (V chased) (NP (Det the) (N dog))))
Number of parses: 1

a dog chased a cat
(S (NP (Det a) (N dog)) (VP (V chased) (NP (Det a) (N cat))))
Number of parses: 1

the dog chased a cat on the mat
(S
  (NP (Det the) (N dog))
  (VP
    (VP (V chased) (NP (Det a) (N cat)))
    (PP (P on) (NP (Det the) (N mat)))))
(S
  (NP (Det the) (N dog))
  (VP
    (V chased)
    (NP (NP (Det a) (N cat)) (PP (P on) (NP (Det the) (N mat))))))
Number of parses: 2

Average parses per sentence: 1.333
2. Program format.
This assignment was quite straight forward making the program quite simple. First off we load the grammar into a NLTK. Next, we create an Earley Chart Parser using this loaded file. Finally, we open the input sentences file and for each sentence, we count the amount of trees and print the desire information along the way. We then add the amount of parse trees for each sentence to a list and at the end caculate the average of that list.
