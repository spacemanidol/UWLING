import sys
import math
from scipy.stats import spearmanr
import pickle

def dot(A,B): 
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
    return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

def readVectors(filename):
    id2vec = []
    word2id = {}
    with open('word2id'+filename, 'r') as f:
        for l in f:
            l = l.strip().split()
            if len(l) == 2:
                word2id[l[0]] = int(l[1])
    with open('vectors'+filename,'r') as f:
        for l in f:
            l = l.strip().split()
            if len(l) > 1:
                id2vec.append([float(i) for i in l])
    return id2vec, word2id

def readTargetWords(filename,index):
    words = []
    with open(filename, 'r') as f:
        if index > 2:
            f.readline() # Simlex has a header
        for l in f:
            l = l.strip().split()
            words.append((l[0],l[1],float(l[index])))
    return words

def createOutput(idx2vector, word2idx, words):
    x, y, other_y = [],[],[]
    count = 0
    for pair in words:
        if pair[0] in word2idx and pair[1] in word2idx:  
            vector1 = idx2vector[word2idx[pair[0]]]
            vector2 = idx2vector[word2idx[pair[1]]]
            x.append(cosine_similarity(vector1,vector2))
            y.append(pair[2])
        else: 
            other_y.append(pair[2])
    average_x = sum(x)/len(x)
    x = x + [average_x for i in range(len(other_y))]
    y = y + other_y
    return spearmanr(x,y)[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: evaluate.py <vector_file>')
        exit(-1)
    else:
        print('Metrics for regular embedding')
        idx2vector, word2idx = readVectors(sys.argv[1])
        print('{}:{}'.format('MEN3k.txt',createOutput(idx2vector, word2idx, readTargetWords('MEN3k.txt',2))))
        print('{}:{}'.format('Simlex999.txt',createOutput(idx2vector, word2idx, readTargetWords('SimLex999.txt',3))))
        print('{}:{}'.format('wordsim353.txt',createOutput(idx2vector, word2idx, readTargetWords('wordsim353.txt',2))))
        print('Metrics for LM enhanced embedding')
#        idx2vector, word2idx = readVectors('LM-'+sys.argv[1])
        print('{}:{}'.format('MEN3k.txt',createOutput(idx2vector, word2idx, readTargetWords('MEN3k.txt',2))))
        print('{}:{}'.format('Simlex999.txt',createOutput(idx2vector, word2idx, readTargetWords('SimLex999.txt',3))))
        print('{}:{}'.format('wordsim353.txt',createOutput(idx2vector, word2idx, readTargetWords('wordsim353.txt',2))))
