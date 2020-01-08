Ling 473 Project 2 Unigrams Counting
Daniel Campos 08/14/2018

## Results table(Just a few) out of the 269225 unique words
the	   4398064
a	   2032214
to	   1893205
of	   1888409
and	   1759680
in	   1486132
that	   814646
for	   793617
is	   712518
on	   564762

## Approach
Find All Files -> Read each file and in each file use regex to->Remove any html tag->Turn anything not an A-Z or ' into a ' '(to help split words)-> Remove trailing and leading ' -> Convert to lower case->Join as text with the same process on all other files->Use Regex to create list of all words-> Loop over said list to get overall count of each unigram-> Output sorted unigrams.

My first step was find a way to get all the files and consume the text. I used pythons os library to get all files in a directory and then read through them. 
Next, I read all the lines in file with f.readlines() which I turn into a long string. After that I use various regex statements to remove all html files, turn illegal characters into spaces, and remove leader and ending '. When this is done convert all text to lower and join with the result of all the other files. Finally I use another regex to get all unique words as a list which I then loop over to get final counts of word occourences. I take this unigram dict and output it in a sorted fashion.
## Special Features
Its super short and concise(again)! Also most of my runs were little over 2 minutes so seems to be a faster solution than my peers found(based on their online comments. Even not minimized code is 28 lines!

## Missing Features
Not robust to errors in input and could probably be optimized much further. 
