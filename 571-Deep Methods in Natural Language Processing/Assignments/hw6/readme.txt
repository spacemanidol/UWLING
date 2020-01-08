Daniel Campos
Ling 571 HW5
10/26/2018
FCFG 
1. Results
John eats
exists e.(eat(e) & eater(e,John))
a student eats
exists x.(student(x) & exists e.(eat(e) & eater(e,x)))
all students eat
all x.(student(x) -> exists e.(eat(e) & eater(e,x)))
John eats a sandwich
exists x.(sandwich(x) & exists e.(eat(e) & eater(e,John) & verbpersonevent(e,x)))
all students eat or drink
all x.(student(x) -> (exists e.(eat(e) & eater(e,x)) | exists e.(drink(e) & drinker(e,x))))
John drinks a soda or eats a sandwich
(exists z3.(soda(z3) & exists e.(drink(e) & drinker(e,John) & verbpersonevent(e,z3))) | exists z2.(sandwich(z2) & exists e.(eat(e) & eater(e,John) & verbpersonevent(e,z2))))
John or Mary eats
(exists e.(eat(e) & eater(e,John)) | exists e.(eat(e) & eater(e,Mary)))
a student writes an essay or eats
exists x.(student(x) & (exists z5.(essay(z5) & exists e.(write(e) & writer(e,x) & verbpersonevent(e,z5))) | exists e.(eat(e) & eater(e,x))))
every student eats a sandwich or drinks a soda
all x.(student(x) -> (exists z8.(sandwich(z8) & exists e.(eat(e) & eater(e,x) & verbpersonevent(e,z8))) | exists z7.(soda(z7) & exists e.(drink(e) & drinker(e,x) & verbpersonevent(e,z7)))))
John eats every sandwich
all x.(sandwich(x) -> exists e.(eat(e) & eater(e,John) & verbpersonevent(e,x)))
John eats every sandwich or bagel
all x.((sandwich(x) | bagel(x)) -> exists e.(eat(e) & eater(e,John) & verbpersonevent(e,x)))
nobody eats a bagel
-exists x z9.(bagel(z9) & exists e.(eat(e) & eater(e,x) & verbpersonevent(e,z9)))
a person does not eat
exists x.(person(x) & -exists e.(eat(e) & eater(e,x)))
Jack does not eat or drink
(-exists e.(eat(e) & eater(e,Jack)) | exists e.(drink(e) & drinker(e,Jack)))
no student eats a bagel
-exists x.(student(x) & exists z10.(bagel(z10) & exists e.(eat(e) & eater(e,x) & verbpersonevent(e,z10))))
2. Approach & Work
a. fcfg grammar
    To solve this problem my approach was much like the last homework where first I made a grammar that could accept all the words and then started tweaking the grammar until I generated parses that produced outputs in the format I desired. I really initially stuggled with the limits of recursion since there were many rules that I thought I had properly simplified but I would get the following error:
    '''  File "/usr/local/lib/python3.6/dist-packages/nltk/sem/logic.py", line 1467, in constants
    return set([self.variable])
    RecursionError: maximum recursion depth exceeded
    '''
b. NLTK Parser: 
    To build this I took my code from hw5 and modified it until I was producing the expected output with the example input files.
3. Problems
    None that I know of. 
4. Insights
    Once again. This hw has highlighted how even when dealing with really small corpuses how hard assembling grammars can be. I imagine that the most scalable solution is to derive solutions that can do so