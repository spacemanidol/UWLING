import array
import collections
import io
try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import scipy.sparse as sp
import numbers

from .glove_cython import fit_vectors

def check_random_state(seed):
    """ Turn seed into a np.random.RandomState instance.

        This is a copy of the check_random_state function in sklearn
        in order to avoid outside dependencies.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)


class Glove(object):
    """
    Class for estimating GloVe word embeddings using the
    corpus coocurrence matrix.
    """

    def __init__(self, no_components=30, learning_rate=0.05,
                 alpha=0.75, max_count=100, max_loss=10.0,
                 random_state=None):
        """
        Parameters:
        - int no_components: number of latent dimensions
        - float learning_rate: learning rate for SGD estimation.
        - float alpha, float max_count: parameters for the
          weighting function (see the paper).
        - float max_loss: the maximum absolute value of calculated
                          gradient for any single co-occurrence pair.
                          Only try setting to a lower value if you
                          are experiencing problems with numerical
                          stability.
        - random_state: random statue used to intialize optimization
        """

        self.no_components = no_components
        self.learning_rate = float(learning_rate)
        self.alpha = float(alpha)
        self.max_count = float(max_count)
        self.max_loss = max_loss

        self.word_vectors = None
        self.word_biases = None

        self.vectors_sum_gradients = None
        self.biases_sum_gradients = None

        self.dictionary = None
        self.inverse_dictionary = None

        self.random_state = random_state

    def fit(self, matrix, epochs=5, no_threads=2, verbose=False):
        """
        Estimate the word embeddings.

        Parameters:
        - scipy.sparse.coo_matrix matrix: coocurrence matrix
        - int epochs: number of training epochs
        - int no_threads: number of training threads
        - bool verbose: print progress messages if True
        """

        shape = matrix.shape

        if (len(shape) != 2 or
            shape[0] != shape[1]):
            raise Exception('Coocurrence matrix must be square')

        if not sp.isspmatrix_coo(matrix):
            raise Exception('Coocurrence matrix must be in the COO format')

        random_state = check_random_state(self.random_state)
        self.word_vectors = ((random_state.rand(shape[0],
                                                self.no_components) - 0.5)
                             / self.no_components)
        self.word_biases = np.zeros(shape[0],
                                    dtype=np.float64)

        self.vectors_sum_gradients = np.ones_like(self.word_vectors)
        self.biases_sum_gradients = np.ones_like(self.word_biases)

        shuffle_indices = np.arange(matrix.nnz, dtype=np.int32)

        if verbose:
            print('Performing %s training epochs '
                  'with %s threads' % (epochs, no_threads))

        for epoch in range(epochs):

            if verbose:
                print('Epoch %s' % epoch)

            # Shuffle the coocurrence matrix
            random_state.shuffle(shuffle_indices)

            fit_vectors(self.word_vectors,
                        self.vectors_sum_gradients,
                        self.word_biases,
                        self.biases_sum_gradients,
                        matrix.row,
                        matrix.col,
                        matrix.data,
                        shuffle_indices,
                        self.learning_rate,
                        self.max_count,
                        self.alpha,
                        self.max_loss,
                        int(no_threads))

            if not np.isfinite(self.word_vectors).all():
                raise Exception('Non-finite values in word vectors. '
                                'Try reducing the learning rate or the '
                                'max_loss parameter.')

    def add_dictionary(self, dictionary):
        """
        Supply a word-id dictionary to allow similarity queries.
        """

        if self.word_vectors is None:
            raise Exception('Model must be fit before adding a dictionary')

        if len(dictionary) > self.word_vectors.shape[0]:
            raise Exception('Dictionary length must be smaller '
                            'or equal to the number of word vectors')

        self.dictionary = dictionary
        if hasattr(self.dictionary, 'iteritems'):
            # Python 2 compat
            items_iterator = self.dictionary.iteritems()
        else:
            items_iterator = self.dictionary.items()
        self.inverse_dictionary = {v: k for k, v in items_iterator}

    def save(self, filename):
        """
        Serialize model to filename.
        """
        with open('vectors'+filename, 'w') as w:
            for i in range(len(self.word_vectors)):
                w.write(' '.join(list(self.word_vectors[i]))+'\n')
        with open('dictionary'+filename, 'w') as f:
            print(self.dictionary)
            pickle.dump(self.dictionary, f, protocol=2)

