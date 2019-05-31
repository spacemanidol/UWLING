import sys
import math
from scipy.stats import spearmanr
import pickle

def dot(A,B): 
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
    return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

def readVectors(vector_file):
    with open('id2word.pkl', 'rb') as f:
        id2word = pickle.load(f)
    with open('word2id.pkl', 'rb') as f:
        word2id = pickle.load(f)    
    with open(vector_file, 'rb') as f:
        word_vectors = pickle.load(f)
    return word_vectors, word2id    

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
    if len(sys.argv) != 5:
        print('Usage: generateCosineDistance.py <vectors_file> <human 1> <human 2> <human 3>')
        exit(-1)
    else:
        idx2vector, word2idx = readVectors(sys.argv[1])
        print('{}:{}'.format(sys.argv[2],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[2],2))))
        print('{}:{}'.format(sys.argv[3],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[3],3))))
        print('{}:{}'.format(sys.argv[4],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[4],2))))
