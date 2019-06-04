import sys

from glove import Glove
from glove import Corpus

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
        corpus_model.load_probs(sys.argv[1])
        corpus_model.fit(read_corpus('text'), window=10)
        print('Dict size: %s' % len(corpus_model.dictionary))
        print('Collocations: %s' % corpus_model.matrix.nnz)
        print('Training the GloVe model')
        glove = Glove(no_components=100, learning_rate=0.05)
        glove.fit(corpus_model.matrix, epochs=25,no_threads=16, verbose=True)
        print_files(glove.word_vectors, corpus_model.dictionary, sys.argv[2])
