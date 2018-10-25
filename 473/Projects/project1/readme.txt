Ling 473 Project 1 Constituent Counting
Daniel Campos 08/02/2018

## Results table
Noun Phrase     13221
Ditransitive Verb Phrase        33
Intransitive Verb Phrase        123
Sentence        4670
Verb Phrase     7920

## Approach
Find All Files -> Read, Normalize and turn into long sentences -> Turn into Trees -> Search Trees for things that match what we are searching for -> reduce lists using lambdas to match desired conditions -> sum over all possible trees
Luck would have it that I actually regularly work with PTB parse trees(search query rewriting) for work which means I was already familiar with various tools that would help me.
My first step was find a way to get all the files and consume the text. I used pythons os library to get all files in a directory and then read through them. 
Next, I read all the lines in file with f.readlines() which produces a list of all the lines. I then use map along with the str.strip tool to remove all trailing spaces and characters and then I join everything in the list to a long string.
Next, I use NLTK's SExpression parser since it is designed to parse sentences with parenthesis and turn my long string into a parsed string. 
After that, since the goal of this project was to count occurrences of specific types of words and in some cases that depending on the preceding context I thought it would be best to use a Parented Tree.
I used NLTK's parented tree since every item has a direct way of searching for its parent node. Then for each tree I use tgrep(a tool deliberatley meant to find POS tags in Trees built into NLTK) to find all parts of a tree that match my desired condition. Finally, I remove all items that dont match my lambda function. The lambda function is none for S, VP, and NP, not having any children for IVP, and len of 3 for DVP.
These operations are performed on every file and subsequently every generated tree to product our output. 

## Special Features
Its super short and concise! Without comments its 36 lines! Python FTW. 

## Missing Features
One thing I did not spend a lot of time on was preparing to deal with any errors in the problem. I assume all files have proper encoding, are readable, etc. I also struggled with condor so I just hardcoded the path of the files within the main.py script. 
Additionally I spent some time debugging what my classmates wrote online since some people got 34 Ditransitive Verbs while I could only find 33. Despite my best efforts, I couldnt get my system to find this hidden DVP :( 
Finally, I have not really done any kind of robust testing(see above) so software provided with no guarentees. 
