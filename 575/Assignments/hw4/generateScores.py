import sys
import math
from scipy.stats import spearmanr
import gensim

def dot(A,B): 
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
    return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

def calc_spearmanr(x,y):
    x_hat = sum(x)/len(x)
    y_hat = sum(y)/len(y)
    p_numerator = 0
    p_denominator_x = 0
    p_denominator_y= 0
    for i in range(len(x)):
        xterm = x[i] - x_hat
        yterm = y[i] - y_hat
        p_numerator += xterm*yterm
        p_denominator_x += xterm**2
        p_denominator_y += yterm**2
    return p_numerator/(math.sqrt(p_denominator_x*p_denominator_y))
def readVectors(filename):
    idx2vector, word2idx=  {}, {}
    index = 0
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split()
            word = l[0]
            vector = [float(i) for i in l[1:]]
            idx2vector[index] = vector
            word2idx[word] = index
            index += 1
    return idx2vector, word2idx        

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
    x, y,other_x, other_y = [],[],[], []
    count = 0
    for pair in words:
        if pair[0] in word2idx and pair[1] in word2idx:  
            vector1 = idx2vector[word2idx[pair[0]]]
            vector2 = idx2vector[word2idx[pair[1]]]
            x.append(cosine_similarity(vector1,vector2))
            y.append(pair[2])
        else: 
            other_y.append(pair[2])
            other_x.append(0)
    other_x = other_x.fill(sum(x)/len(x))
    x = x + other_x
    y = y + other_y
    return spearmanr(x,y)[0]

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Usage: generateCosineDistance.py <vectors_file> <human 1> <human 2> <human 3>')
        exit(-1)
    else:
        idx2vector, word2idx = readVectors(sys.argv[1])
        #model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True) 
        print('{}:{}'.format(sys.argv[2],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[2],2))))
        print('{}:{}'.format(sys.argv[3],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[3],3))))
        print('{}:{}'.format(sys.argv[4],createOutput(idx2vector, word2idx, readTargetWords(sys.argv[4],2))))