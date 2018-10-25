Ling 473 Project 4 DNA Search
Daniel Campos 08/30/2018

## Results Just a few lines
target_files/chr1.dna
	0000C312	AAACTAACTGAATGTTAGAACCAACTCCTGATAAGTCTTGAACAAAAG
	00022723	GGGGCTGGAGACTGACTTAATCACCAACAGCCAAAGGTTTTATCAATCATGCTTGCATAATAAAGCCTC
	00071235	CATATATAAAAAATGAAACTGTGACCGATTTTAAGGACAGTATTGGCAAATATTTCTGTGCTCTTGGAGGAGAAGACCCTTATTGG
	000A53CA	GGGGCTGGAGACTGACTTAATCACCAACAGCCAAAGGTTTTATCAATCATGCTTGCATAATAAAGCCTC
	0014CFE3	AGCTCTGGAAATCCCTCAACAATTGTGTCCAGTTTCACCACGAA

## Approach
My approach to this project was to make a simple program first and then iterate on how to optimize and speed it up. 
I started by implementing a node and a trie class in the simplest wayI could imagine. I did so by just having a node include a pointer to its children node, and if they are a final node. Then I made a trie class that has a method that adds a word to a trie. Using these classes I read all the target strings in the target sequences files and load them into the trie. Next, for each file in our target corpus folder we load open each file and read all the contents into a string. Then at each step in the string (represented by variable i)we try to traverse our tree to find one of our target sequences. If we ever break from our target sequence, we break from our trie search move to i+1 and start our search again. If we find a target sequence we output the result and move the i to the end of that target sequence, which is since no sequence can contain subsequences of other strings. During the entire process we are converting all characters to upper case and ignore any character that is not a ACGT. 

For the extra credit I just created a dict where the key is the target sequence and the value is a list of the offset plus the filename. When a sequence is found we just add its location(offset and filename) to our dict's value's list. Once we have finished finding all sequences we loop over our dict and print out results. 

During the entire process my approach was always start dirty and then optimize. I used tools like cProfile which helped me indentify inefficiencies in my code. One of the bigest examples was at one point I was comparing my i and j values to len(input_text) at every step. This calulation was meaning that at each step in my code we had to one calculate the length of text and then see if our i or j was larger. By saving len(input_text) to a variable and comparing that at each time my program ran 30% faster. I applied this sort of effort to the entire program and slowly went optimizing my code to its state now. That being said, for this program it seems that python was a terrible choice and I should have just bitten the bullet and written it in C which would have made my runtime in seconds or minutes istead of the ~ 70 minutes it currently runs in. Worth noting, on my personal rig the chr19 runs in ~110 seconds but on condor it runs in ~ 220 seconds. Same for the entire assignment. Personal device runs ~ 70 minutes and ~3 hours on condor. 
 

## Special Features
No Special Features

## Missing Features
Speed Optimizations, robust error handling



