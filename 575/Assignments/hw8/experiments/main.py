import sys
import math
from scipy.stats import spearmanr

from glove import Glove
from glove import Corpus

def dot(A,B):
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
    return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

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

def readTargetWords(filename,index):
    words = []
    with open(filename, 'r') as f:
        if index > 2:
            f.readline() # Simlex has a header
        for l in f:
            l = l.strip().split()
            words.append((l[0],l[1],float(l[index])))
    return words

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

def read_corpus(filename):
    delchars = [chr(c) for c in range(256)]
    delchars = [x for x in delchars if not x.isalnum()]
    delchars.remove(' ')
    delchars = ''.join(delchars)
    with open(filename, 'r') as datafile:
        for line in datafile:
            yield line.lower().translate(None, delchars).split(' ')

def print_files(wordvectors, word2id, filename):
    with open('vectors' + filename, 'w') as w:
        for i in range(len(wordvectors)):
            l = wordvectors[i].tolist()
            out = ''
            for j in range(len(l)):
                out += str(l[j])
                out += ' '
            w.write('{}\n'.format(out[:-1]))
    with open('word2id' + filename, 'w') as w:
        for key in word2id:
            w.write('{} {}\n'.format(key, word2id[key]))

if __name__ == '__main__':
        corpus_model = Corpus()
        corpus_model.load_probs('nonprobs')
        corpus_model.fit(read_corpus('text'), window=10)
        print('Dict size: %s' % len(corpus_model.dictionary))
        print('Collocations: %s' % corpus_model.matrix.nnz)
        print('Training the GloVe model')
        glove = Glove(no_components=100, learning_rate=0.05)
        glove.fit(corpus_model.matrix, epochs=25,no_threads=16, verbose=True)
        print_files(glove.word_vectors, corpus_model.dictionary, sys.argv[2])
        print('Metrics for regular embedding')
        print('{}:{}'.format('evalfiles/MEN3k.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/MEN3k.txt',2))))
        print('{}:{}'.format('evalfiles/Simlex999.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/SimLex999.txt',3))))
        print('{}:{}'.format('evalfiles/wordsim353.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/wordsim353.txt',2))))
        corpus_model = Corpus()
        corpus_model.load_probs(sys.argv[1])
        corpus_model.fit(read_corpus('text'), window=10)
        print('Dict size: %s' % len(corpus_model.dictionary))
        print('Collocations: %s' % corpus_model.matrix.nnz)
        print('Training the GloVe model')
        glove = Glove(no_components=100, learning_rate=0.05)
        glove.fit(corpus_model.matrix, epochs=25,no_threads=16, verbose=True)
        print_files(glove.word_vectors, corpus_model.dictionary, 'LM-' + sys.argv[2])
        print('Metrics for LM enhanced embedding')
        print('{}:{}'.format('evalfiles/MEN3k.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/MEN3k.txt',2))))
        print('{}:{}'.format('evalfiles/Simlex999.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/SimLex999.txt',3))))
        print('{}:{}'.format('evalfiles/wordsim353.txt',createOutput(glove.word_vectors, corpus_model.dictionary, readTargetWords('evalfiles/wordsim353.txt',2))))
