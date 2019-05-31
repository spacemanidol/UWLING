import sys

from collections import Counter

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
    pairs = set()
    with open(corpus, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip().split()
            for center_i, center_word in enumerate(l):
                if center_word in vocab:
                    center_id = vocab[center_word]
                    context_ids = l[max(0, center_i - window_size) : center_i]
                    contexts_len = len(context_ids)
                    for left_i, left_word in enumerate(context_ids):
                        if left_word in vocab:
                            pairs.add((left_word, center_word))
                            pairs.add((center_word, left_word))
    with open('pairs','w', encoding='utf-8') as w:
        for p in pairs:
            w.write("{} {}\n".format(p[0],p[1]))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:python generate_pairs <corpus> <min_count> <window_size>")
        exit(-1)
    else:
        build_vocab(sys.argv[1], sys.argv[2])
        build_cooccur(load_vocab(), sys.argv[1], sys.arv[3])