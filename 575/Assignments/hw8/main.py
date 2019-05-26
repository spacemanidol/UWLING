import math
import pickle
import numpy as np

from collections import Counter
from random import shuffle
from scipy import sparse
from LM import LM, BERTLM

def build_vocab(corpus):
    """
    Build a vocabulary with word frequencies for an entire corpus.
    Returns a dictionary `w -> (i, f)`, mapping word strings to pairs of
    word ID and word corpus frequency.
    """
    vocab = Counter()
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            tokens = l.strip().split()
            vocab.update(tokens)
    return {word: (i, freq) for i, (word, freq) in enumerate(vocab.items())}

def build_cooccur(vocab, corpus, window_size, min_count, lm):
    """
    Build a word co-occurrence list for the given corpus.
    """
    vocab_size = len(vocab)
    id2word = dict((i, word) for word, (i, _) in vocab.items())
    cooccurrences = sparse.lil_matrix((vocab_size, vocab_size),dtype=np.float64)
    i = 0
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            if i % 1000 == 0:
                print("Building cooccurrence matrix: on line {}".format(i))
            i += 1
            l = l.strip()
            tokens = l.split()
            token_ids = [vocab[word][0] for word in tokens]
            for center_i, center_id in enumerate(token_ids):
                context_ids = token_ids[max(0, center_i - window_size) : center_i]
                contexts_len = len(context_ids)
                for left_i, left_id in enumerate(context_ids):
                    distance = contexts_len - left_i
                    increment = 1.0 / float(distance)
                    cooccurrences[center_id, left_id] += increment
                    cooccurrences[left_id, center_id] += increment
                    #cooccurrences[center_id, left_id] += increment * math.exp(lm.check_probabilities(' '.join([id2word[center_id]] + [id2word[left_id]]))['real_topk'][1][1])
                    #cooccurrences[left_id, center_id] += increment  * math.exp(lm.check_probabilities(' '.join([id2word[left_id]] + [id2word[center_id]]))['real_topk'][1][1])
    for i, (row, data) in enumerate(zip(cooccurrences.rows,cooccurrences.data)):
        if min_count is not None and vocab[id2word[i]][1] < min_count:
            continue
        for data_idx, j in enumerate(row):
            if min_count is not None and vocab[id2word[j]][1] < min_count:
                continue
            yield i, j, data[data_idx]

def run_iter(vocab, data, learning_rate, x_max=100, alpha=0.75):
    """
    Run a single iteration of GloVe training
    """
    global_cost = 0
    shuffle(data)
    for (v_main, v_context, b_main, b_context, gradsq_W_main, gradsq_W_context,
        gradsq_b_main, gradsq_b_context, cooccurrence) in data:
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
        with open('model'+str(i), 'wb') as vector_f:
            pickle.dump(W, vector_f, protocol=2)
        print("\t\tDone (loss {}".format(run_iter(vocab, data, learning_rate)))
    return W
    
def main(corpus='text1', vector_size=50, iterations=2, learning_rate=0.05, window_size=5,min_count=1):
    print("Building Vocab")
    vocab = build_vocab(corpus)
    print("{} words in vocabulary".format(len(vocab)))
    lm = LM()
    #bertlm = BERTLM()
    cooccurrences = list(build_cooccur(vocab, corpus, window_size, min_count,lm))
    print("Training Embeddings")
    W = train(vocab, cooccurrences, vector_size, iterations, learning_rate)
    with open('model', 'wb') as vector_f:
        pickle.dump(W, vector_f, protocol=2)

if __name__ == '__main__':
    main()
