from __future__ import print_function

import os
import sys
import re
import nltk
import numpy as np
import xml.sax.saxutils as saxutils

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Input, GlobalAveragePooling1D, Embedding
from sklearn.utils import column_or_1d
from bs4 import BeautifulSoup

EPOCHS = 5
SUBSAMPLE = .982
EMBEDDING_DIM = 100
MAX_SEQUENCE_LENGTH = 100
MAX_NUM_WORDS = 400000
OPTIMIZER = 'rmsprop'
ACTIVATION = 'softmax'
LOSSFUNCTION = 'categorical_crossentropy'

def transform(target, y):
    y = column_or_1d(y, warn=True)
    indices = np.isin(y, target)
    y_transformed = np.searchsorted(target, y)
    y_transformed[~indices]=-1
    return y_transformed

def loadVectors(filename):
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

def unescape(text):
    """Unescape charactes."""
    return saxutils.unescape(text)

def strip_tags(text):
    """String tags for a better vocabulary."""
    return re.sub('<[^<]+?>', '', text).strip()

def read_reuters_files(path="./reuters-21578/"):
    x_train, x_test, y_train,y_test = {}, {}, {}, {}
    for file in os.listdir(path):
        if file.endswith(".sgm"):
            print("reading ", path + file)
            f = open(path + file, 'r')
            data = f.read()
            soup = BeautifulSoup(data, 'lxml')
            posts = soup.findAll("reuters")
            for post in posts:
                post_id = post['newid']
                body = unescape(strip_tags(str(post('text')[0])).replace('reuter\n&#3;', ''))
                topics = post.topics.contents
                if len(topics) == 0:
                    topics = 'Other'
                else:
                    topics = topics[0]
                if post["lewissplit"] == "TRAIN":
                    x_train[post_id] = body
                    y_train[post_id] = topics
                else:
                    x_test[post_id] = body
                    y_test[post_id] = topics
        nx_train, ny_train, nx_test, ny_test = [], [], [], []
        for i in x_train:
            nx_train.append(x_train[i])
            ny_train.append(y_train[i])
        for i in x_test:
            nx_test.append(x_test[i])
            ny_test.append(y_test[i])
    return nx_train, ny_train, nx_test, ny_test

def run(id2vec,word2id,x_train, y_train, x_test, y_test):
    embeddings_index_len = len(id2vec)
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    all_classes = list(set(y_train))
    num_classes = len(all_classes) + 1
    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=MAX_SEQUENCE_LENGTH)
    x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=MAX_SEQUENCE_LENGTH)
    y_train = to_categorical(np.asarray(transform(np.array(all_classes), y_train)), num_classes=num_classes)
    y_test = to_categorical(np.asarray(transform(np.array(all_classes), y_test)), num_classes=num_classes)
    indices = np.arange(x_train.shape[0])
    np.random.shuffle(indices)
    x_train = x_train[indices]
    y_train = y_train[indices]
    subsampled_size = int(SUBSAMPLE * x_train.shape[0])
    x_train = x_train[:-subsampled_size]
    y_train = y_train[:-subsampled_size]
    print('{} new size x_Train'.format(len(x_train)))
    num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
    embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, EMBEDDING_DIM))
    for word, i in word2id.items():
        if i > MAX_NUM_WORDS:
            continue
        index = word_index.get(word)
        if index is not None:
            embedding_matrix[index] = id2vec[i]
    model = Sequential()
    model.add(Embedding(num_words,  EMBEDDING_DIM, weights=[embedding_matrix], trainable=False))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(num_classes, input_shape=(100,),activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(x_train, y_train, epochs=1)
    print('Test accuracy:', model.evaluate(x_test, y_test))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: model.py <vectors_file>')
        exit(-1)
    else:
        x_train, y_train, x_test, y_test = read_reuters_files()
        print('Regular')
        id2vec, word2id = loadVectors(sys.argv[1])
        run(id2vec, word2id,x_train, y_train, x_test, y_test)
        print("LM Based")
        id2vec, word2id = loadVectors('LM-' + sys.argv[1])
        run(id2vec, word2id,x_train, y_train, x_test, y_test)
