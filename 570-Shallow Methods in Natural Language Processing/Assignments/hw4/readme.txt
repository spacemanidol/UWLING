In your note file, explain briefly how the fsm produced by expand_fsm1.sh differs
from the one produced by expand_fsm2.sh.
Ling 570 HW4 FSM expander and acceptor
Daniel Campos
10/25/2018

## Approach
My approach to morph acceptor was just to expand my hw2 and hw3 acceptor so it was quite simple. For the expand_fsm my approach was to load the lexicon, 
load the morph and then replace the morph with all the words that matched the morph rule. In other words regular_verb_stem going from g0 to q1 become 4 
and the accetable transiitons became the words instead of the morph type. Next, once I verified this worked, I took this modified fsm from a word level to character.
In other words, for each state if the word was cut I split that into 5 states: first state is (q0 (q0_c_cut *e*)) in other words go to the next letter in the word. 
Then I created states (q0_c_cut (q0_u_cut c)) and so on for each letter. Then final state was (q0_t_cut (q1 *e*)). In other words after something has followed the whole path it can transition to the next regular state. See below for what I mean. 
example 
(q0 (q0_caught_c *e*))
(q0_caught_c (q0_caught_a c))
(q0_caught_a (q0_caught_u a))
(q0_caught_u (q0_caught_g u))
(q0_caught_g (q0_caught_h g))
(q0_caught_h (q0_caught_t h))
(q0_caught_t (q3 t))
## Difference between expand_fsm1 and fsm2
The differences between expand_fsm1 and fsm2 were suttle but it was mostly based on how I delt with saving the morphology. In expand_fsm1 I didnt care about the morph rules and I dropped them. In expand_fsm2 I needed 
to preserve them so I followed the same process as mentioned above but every state except the final(micro final, from last word specific letter to next real state) state adds a "*e*", see below for actual example. Then since I did this transition I had to do some specific formating things in my morph_acceptor2. 


Example 
(q0 (q0_caught_c *e* *e*))
(q0_caught_c (q0_caught_a c *e*))
(q0_caught_a (q0_caught_u a *e*))
(q0_caught_u (q0_caught_g u *e*))
(q0_caught_g (q0_caught_h g *e*))
(q0_caught_h (q0_caught_t h *e*))
(q0_caught_t (q3 t irreg_past_verb_form))