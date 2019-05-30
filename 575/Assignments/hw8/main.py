import math
import pickle
import numpy as np

from collections import Counter
from random import shuffle
from scipy import sparse
from LM import LM, BERTLM

def build_vocab(corpus='text', min_count=5):
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

def build_cooccur(vocab, corpus='text', window_size=5, uselm = False):
    """
    Build a word co-occurrence list for the given corpus.
    """
    if uselm == True:
        lm = LM()
    vocab_size = len(vocab)
    cooccurrences = np.ndarray((vocab_size, vocab_size),dtype=np.float64)
    i = 0
    probs = {}
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            if i % 1000 == 0:
                print("Building cooccurrence matrix: on line {}".format(i))
            i += 1
            l = l.strip().split()
            for center_i, center_word in enumerate(l):
                if center_word in vocab:
                    center_id = vocab[center_word]
                    context_ids = tokens[max(0, center_i - window_size) : center_i]
                    contexts_len = len(context_ids)
                    for left_i, left_word in enumerate(context_ids):
                        if left_word in vocab:
                            distance = contexts_len - left_i
                            increment = 1.0 / float(distance)
                            left_id = vocab[left_word]
                            if (center_word,left_word) not in probs:
                                temp = math.exp(lm.generate_conditionalprobs(center_word,left_word)+lm.generate_conditionalprobs(center_word,left_word))
                                probs[(center_word,left_word)] = temp 
                                probs[(left_word,center_word)] = temp
                            if uselm == True:
                                cooccurrences[center_id, left_id] += increment * probs[(center_word,left_word)]
                                cooccurrences[left_id, center_id] += increment * probs[(center_word,left_word)]
                            else:
                                cooccurrences[center_id, left_id] += increment
                                cooccurrences[left_id, center_id] += increment 
    return cooccurrences

def save_cooccur(data):
    length, width = data.shape 
    with open('coocur.txt','w') as w:
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
        cost_inner = (v_main.dot(v_context) + b_main[0] + b_context[0] - math.log(cooccurrence))
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

def train(vocab, cooccurrences, vector_size,iterations, learning_rate):
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
    data = [(W[i_main], W[i_context + vocab_size],biases[i_main : i_main + 1], biases[i_context + vocab_size : i_context + vocab_size + 1],gradient_squared[i_main], gradient_squared[i_context + vocab_size], gradient_squared_biases[i_main : i_main + 1],gradient_squared_biases[i_context + vocab_size: i_context + vocab_size + 1],cooccurrence) for i_main, i_context, cooccurrence in cooccurrences]
    for i in range(iterations):
        print("\tBeginning iteration {}..".format(i))
        print("\t\tDone (loss {}".format(run_iter(vocab, data, learning_rate)))
    return W

def main(corpus='text', vector_size=50, iterations=15, learning_rate=0.05, window_size=5,min_count=5):
    print("Building Vocab")
    vocab = build_vocab(corpus)
    vocab = load_vocab()
    print("{} words in vocabulary".format(len(vocab)))
    id2word = dict((i, word) for word, i in vocab.items())
    word2id = dict((word,i) for word,  i in vocab.items())    
    cooccurrences = build_cooccur(vocab,id2word, corpus, window_size, min_count)

    print("Training Embeddings")
    W = train(vocab, cooccurrences, vector_size, iterations, learning_rate)
    with open('id2word.pkl', 'wb') as f:
        id2word = pickle.load(f)
    with open('word2id.pkl', 'wb') as f:
        word2id = pickle.load(f) 
    with open('glove_vectors.pkl', 'wb') as vector_f:
            pickle.dump(W, vector_f, protocol=2)

if __name__ == '__main__':
    main()
