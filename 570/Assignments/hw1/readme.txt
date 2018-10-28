Ling 570 HW1 Tokenizer and Unigram Counter
Daniel Campos 10/04/2018
Q1
For my tokenizer I started off with a naive implementation. I would start with the slides in day01-token.pdf and generated some regex rules. Once I had generated what I beleived to be enough regex rules I then thought of other possible scenarios and how this would influence my parser. Finally I read all the abbreviations from the Abbreviation file given, turn them into compiled regex parameters and load them into a list.

Once I had all these regex patterns I then moved onto the input. I load in each line, split on whitespace into a list and then for each item in the list I loop over it and try all of my regex rules, it there is a match for something like url or email I keep it in its current form, if there is no match then I split with regular rules around punctuation. 

Once I was done and I compared the sizes of ex2 vs ex2.tok it was crazy that the amount of tokens had increased ~15%. 

Q2
For the voc counter I took a basic approach and split on whitespace and then kept tract of occourences in a dict. It was quite fast and effective and to the point. Swinging in the opposite direction of Q1 I was surprised that by running my vocabulary frequency calculator the amount of words decreased from 10425 to 7850 so almost 25%! Crazy 

Q3 
A) i)Number Of Token in ex2 = 39824
   ii)Number of Tokens in ex2.tok = 47224
B) i)Number of Lines in ex2.voc = 10425
   ii)Number of Lines in ex2.tok.voc = 7850
