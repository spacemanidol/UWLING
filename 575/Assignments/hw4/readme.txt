First conver Binary word2vec to text
```
python convertWord2VecBinToTxt.py ../vectors/<file>.bin ../vectors/<file>.txt
```
run evaluation
```
python generateScores.py ../vectors/gloveuncleaned.txt MEN3k.txt SimLex999.txt wordsim353.txt
```
Submit a result.txt to me with the content covering
1. The results from five embeddings (4 word2vec and 1 GloVe);
2. Your observations on HS v.s. NS on CBOW and SG, as well as the comparison to GloVe.
NOTE: For each evaluation benchmark dataset, you need to have 5 scores. I strongly recommend that you use a table to accommodate the scores.
Table
Model Name | glove | HS SG | HS CBOW | NS SG | NS CBOW | Normal SG | Normal CBOW 
MEN3K.txt | 0.37941| 0.67656 | 0.60360 | 0.67148 | 0.66224 | 0.01081 | 0.01081
SimLex999.txt | 0.16883 | 0.25066 | 0.22989 | 0.28304 | 0.29605 | -0.01391 | -0.01391
wordsim353.txt | 0.39860 | 0.69251 | 0.69002 | 0.70646 | 0.71728 | -0.021834 | -0.021834


