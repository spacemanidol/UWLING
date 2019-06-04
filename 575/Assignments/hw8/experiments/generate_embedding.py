import math
import sys
import pickle
import numpy as np

from collections import Counter
from random import shuffle
#from scipy import sparse

def build_vocab(corpus, min_count):
    """
    Build a vocabulary with word frequencies for an entire corpus.
    Returns a dictionary `w -> (i, f)`, mapping word strings to pairs of
    word ID and word corpus frequency. When done save to vocab file
    """
    vocab = Counter()
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            vocab.update(l.strip().split())
    i = 0
    with open('vocab.txt', 'w', encoding='utf-8') as w:
        for word in sorted(vocab, key=vocab.get ,reverse=True):
            if vocab[word] == min_count:
                break
            w.write('{}\t{}\t{}\n'.format(word,vocab[word],i))
            i += 1

def load_vocab():
    """
    Load vocabulary created earlier. 
    """
    vocab = {}
    with open('vocab.txt', 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip().split('\t')
            vocab[l[0]] = (int(l[2]))
    return vocab

def build_cooccur(vocab, corpus, window_size):
    """
    Build a word co-occurrence list for the given corpus.
    """
    vocab_size = len(vocab)
    cooccurrences  = {}
    i = 0
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            if i % 1000 == 0:
                print("Building cooccurrence matrix: on line {}".format(i))
            i += 1
            l = l.strip().split()
            for center_i, center_word in enumerate(l):
                if center_word in vocab:
                    center_id = vocab[center_word]
                    context_ids = l[max(0, center_i - window_size) : center_i]
                    contexts_len = len(context_ids)
                    for left_i, left_word in enumerate(context_ids):
                        if left_word in vocab:
                            distance = contexts_len - left_i
                            increment = 1.0 / float(distance)
                            left_id = vocab[left_word]
                            if (center_id,left_id) in cooccurrences:
                                cooccurrences[(center_id, left_id)] += increment
                                cooccurrences[(left_id, center_id)] += increment
                            else:
                                cooccurrences[(center_id, left_id)] = increment
                                cooccurrences[(left_id, center_id)] = increment
    return cooccurrences

def load_condprob(filename):
    probs = {}
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split()
            if len(l) == 3:
                probs[(l[0],l[1])] = float(l[2])
    return probs

def update_weights(data, id2word, probsfilename):
    length = len(data)
    probs = load_condprob(probsfilename)
    print("{} existing condprobs loaded".format(len(probs)))
    for i in range(length):
        if i in id2word:
            left_word = id2word[i]
            if i % 1000 ==  0:
                print("{} rows done".format(i))
            for j in range(length):
                if (i,j) in data and j in id2word and  data[(i,j)] > 0:
                    right_word = id2word[j]
                    p1,p2 = 1,1
                    if (left_word,right_word) in probs:
                        p1 = probs[(left_word,right_word)]
                    if (right_word,left_word) in probs:
                        p2 = probs[(right_word,left_word)]
                    temp = math.exp(p1+p2)
                    data[(i, j)] *= temp
    return data

def save_cooccur(data, filename):
    length, width = data.shape 
    with open(filename,'w') as w:
        for i in range(length):
            out = ''
            for j in range(width):
                out += '{} '.format(data[i][j])
            w.write(out[:-1]+'\n')

def load_cooccur(vocab_size):
    data = np.array(vocab_size)
    with open('coocur.txt','r') as f:
        for l in f:
            l = l.strip().split(' ')
            data.append(np.array(l),dtype=np.float64)
    return data

def run_iter(vocab, data, learning_rate, x_max=100, alpha=0.75):
    """
    Run a single iteration of GloVe training
    """
    global_cost = 0
    shuffle(data)
    for (v_main, v_context, b_main, b_context, gradsq_W_main, gradsq_W_context, gradsq_b_main, gradsq_b_context, cooccurrence) in data:
        weight = (cooccurrence / x_max) ** alpha if cooccurrence < x_max else 1
        tmp = 0
        if cooccurrence > 0:
            tmp = math.log(cooccurrence)
        cost_inner = (v_main.dot(v_context) + b_main[0] + b_context[0] - tmp)
        cost = weight * (cost_inner ** 2)
        global_cost += 0.5 * cost
        grad_main = weight * cost_inner * v_context
        grad_context = weight * cost_inner * v_main
        grad_bias_main = weight * cost_inner
        grad_bias_context = weight * cost_inner
        v_main -= (learning_rate * grad_main / np.sqrt(gradsq_W_main))
        v_context -= (learning_rate * grad_context / np.sqrt(gradsq_W_context))
        b_main -= (learning_rate * grad_bias_main / np.sqrt(gradsq_b_main))
        b_context -= (learning_rate * grad_bias_context / np.sqrt(gradsq_b_context))
        gradsq_W_main += np.square(grad_main)
        gradsq_W_context += np.square(grad_context)
        gradsq_b_main += grad_bias_main ** 2
        gradsq_b_context += grad_bias_context ** 2
    return global_cost

def train(vocab, cooccurrences, vector_size, iterations=15, learning_rate=0.05):
    """
    Train word embedding via word cooccurrences each element is of the form (word_i, word_j, x_ij)
    where `x_ij` is a cooccurrence value $X_{ij}$ as noted Pennington et al. (2014)
    Returns word vector matrix `W`.
    """
    vocab_size = len(vocab)
    W = (np.random.rand(vocab_size * 2, vector_size) - 0.5) / float(vector_size + 1)
    biases = (np.random.rand(vocab_size * 2) - 0.5) / float(vector_size + 1)
    gradient_squared = np.ones((vocab_size * 2, vector_size),dtype=np.float64)
    gradient_squared_biases = np.ones(vocab_size * 2, dtype=np.float64)
    print("creating data")
    data = [(W[i_main], W[i_context + vocab_size],biases[i_main : i_main + 1], biases[i_context + vocab_size : i_context + vocab_size + 1],gradient_squared[i_main], gradient_squared[i_context + vocab_size], gradient_squared_biases[i_main : i_main + 1],gradient_squared_biases[i_context + vocab_size: i_context + vocab_size + 1],cooccurrence) for (i_main, i_context), cooccurrence in cooccurrences.items()]
    for i in range(iterations):
        print("\tBeginning iteration {}..".format(i))
        print("\t\tDone (loss {}".format(run_iter(vocab, data, learning_rate)))
    return W

def main(corpus, min_count, window_size, probs_filename, vector_size, vector_name):
    print("Building Vocab")
    build_vocab(corpus, min_count)
    vocab = load_vocab()
    id2word = dict((i, word) for word, i in vocab.items())
    word2id = dict((word, i) for word, i in vocab.items())
    print("{} words in vocabulary".format(len(vocab)))  
    cooccurrences = build_cooccur(vocab, corpus, window_size)
    print("Training LM enhanced Embeddings")
    WLM = train(vocab, update_weights(cooccurrences, id2word, probs_filename), vector_size)
    with open(vector_name + '-id2word.pkl', 'wb') as f:
        pickle.dump(id2word, f, protocol=2)
    with open(vector_name + '-word2id.pkl', 'wb') as f:
        pickle.dump(word2id, f, protocol=2)
    with open('LM-' + vector_name, 'wb') as vector_f:
        pickle.dump(WLM, vector_f, protocol=2) 
    print("Training Embeddings")
    W = train(vocab, cooccurrences, vector_size)
    with open(vector_name, 'wb') as vector_f:
        pickle.dump(W, vector_f, protocol=2) 

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Usage:python generate_embedding.py <corpus> <min_count> <window_size> <probs_filename> <vector_size> <vector_name>")
        exit(-1)
    else:
        main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],int(sys.argv[5]),sys.argv[6])
