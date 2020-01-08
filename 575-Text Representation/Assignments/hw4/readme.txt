HW4 Glove Vs word2vec

For this homework the goal was to explore implementation of Word2Vec and Glove. 

To train glove, I used my previous encodings which was based on the the cleaned version of enwik8. I did this since training of the non preprocessed version seemed to take much longer for non increased performance. 
This cleaning used the perl script to remove html and other website related tags. 
Next, I trained the various glove methods with similair setting to Glove. That is to say, 15 iterations, a window size of 8, vector size of 200 and a min vocabulary of 1. 
For the sub settings in Word2vec I used Hierarchical Softmax(HS) with no negative sampling(NS), and for NS I set N=25. 
To get a further baseline, I also trained Word2vec with no HS and no NS.

## Results
Model performance can be found below but in general, the Skipgram(SG) outperforms the Continous Bag Of Words(CBOW) but not by much. 
We can also see that in general word2vec outperforms glove but only when using HS or NS. Without its modifications, Word2Vec performs much worse than glove.
My suspicion is eventually the plain word2vec implementation could match the accuracy but it would require 10x the iterations.
Across all the evaluations it seems the best model is NS SG. This may change with different sampling rates and training length but given the current parameters it seems to be the most effective.
When I looked into more about why this may be the best results the literature seemed to present that SG and NS can learn a more fine grained relation of words.

Model Name | glove | HS SG | HS CBOW | NS SG | NS CBOW | Normal SG | Normal CBOW 
MEN3K.txt | 0.37941| 0.67656 | 0.60360 | 0.67148 | 0.66224 | 0.01081 | 0.01081
SimLex999.txt | 0.16883 | 0.25066 | 0.22989 | 0.28304 | 0.29605 | -0.01391 | -0.01391
wordsim353.txt | 0.39860 | 0.69251 | 0.69002 | 0.70646 | 0.71728 | -0.021834 | -0.021834
## Implementation.
I made 2 python scripts and a few bash scripts. The pythons scripts usage is bellow. 
First conver Binary word2vec to text
```
python convertWord2VecBinToTxt.py ../vectors/<file>.bin ../vectors/<file>.txt
```
run evaluation
```
python generateScores.py ../vectors/gloveuncleaned.txt MEN3k.txt SimLex999.txt wordsim353.txt
```



