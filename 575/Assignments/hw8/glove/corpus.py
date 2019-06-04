import numpy as np
try:
    import cPickle as pickle
except ImportError:
    import pickle

from .corpus_cython import construct_cooccurrence_matrix

class Corpus(object):
    def __init__(self):
        self.dictionary = {}
        self.dictionary_supplied = False
        self.matrix = None
        self.probs = {}
    def load_probs(self, filename):
        with open('probs','r') as f:
            for l in f:
                l = l.strip().split()
                if len(l) == 3:
                    self.probs[(l[0],l[1])] = float(l[2])
        print('{} examples loaded'.format(len(self.probs)))

    def fit(self, corpus, window=10, ignore_missing=False):
        self.matrix = construct_cooccurrence_matrix(corpus,self.dictionary,self.probs,int(self.dictionary_supplied),int(window),int(ignore_missing))
    def save(self, filename):
        with open('matrix-' + filename, 'wb') as f:
            pickle.dump(self.matrix, f, protocol = 2)
        with open('dict-' + filename, 'wb') as f:
            pickle.dump(self.dictionary, f, protocol = 2)
        with open(filename, 'wb') as savefile:
            pickle.dump((self.dictionary, self.matrix),savefile,protocol=pickle.HIGHEST_PROTOCOL)
    @classmethod
    def load(cls, filename):
        instance = cls()
        with open(filename, 'rb') as savefile:
            instance.dictionary, instance.matrix = pickle.load(savefile)
        return instance
