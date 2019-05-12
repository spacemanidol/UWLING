from __future__ import print_function

import os
import sys
import math
import numpy as np
import skipthoughts

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Input, GlobalMaxPooling1D, MaxPooling1D, Embedding, Conv1D, LSTM, Bidirectional, Flatten, Lambda
from sklearn.utils import column_or_1d

from keras import backend as K

EPOCHS = 20
EMBEDDING_DIM = 200
MAX_SEQUENCE_LENGTH = 50
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
    embeddings_index = {}
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            embeddings_index[l[0]] = np.array([np.float32(i) for i in l[1:]])
    return embeddings_index

train_data_filename = 'SICK_train.txt'
test_data_filename = 'SICK_test_annotated.txt'

def loadData(train_data_filename, test_data_filename, embeddings_index):
model = skipthoughts.load_model()
encoder = skipthoughts.Encoder(model)

embeddings_index_len = len(embeddings_index)
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
x_train, y_train, x_test, y_test = [], [], [], []
with open(train_data_filename, 'r') as f:
    f.readline()# header
    for l in f:
        l = l.strip().split('\t')
        x_train.append(' '.join(l[1:3]))
        y_train.append(l[4])


with open(test_data_filename,'r') as f:
    f.readline()# header
    for l in f:
        l = l.strip().split('\t')
        x_test.append(' '.join(l[1:3]))
        y_test.append(l[4])

x_train_skipthought = encoder.encode(x_train)
x_test_skipthought = encoder.encode(x_test)
all_classes = list(set(y_train))
num_classes = len(all_classes) + 1
tokenizer.fit_on_texts(x_train)
word_index = tokenizer.word_index
x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=MAX_SEQUENCE_LENGTH)
x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=MAX_SEQUENCE_LENGTH)
y_train = to_categorical(np.asarray(transform(np.array(all_classes), y_train)), num_classes=num_classes)
y_test = to_categorical(np.asarray(transform(np.array(all_classes), y_test)), num_classes=num_classes)
yt = y_train[:100]
yte = y_test[:100]
num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    if i > MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector


def create_and_model(x_test, x_train,y_test, y_train, num_words, embedding_matrix, embedding_dim, num_classes):
model = Sequential()
model.add(Embedding(num_words,  embedding_dim, weights=[embedding_matrix], trainable=True))
model.add(Lambda(function=lambda x: (K.sum(x, axis=1))/math.sqrt(MAX_SEQUENCE_LENGTH), output_shape=lambda shape: (shape[0],) + shape[2:]))
model.add(Dense(num_classes, activation=ACTIVATION))
model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
model.fit(x_train, y_train, epochs=EPOCHS)
print('Test accuracy:', model.evaluate(x_test, y_test)[1])


model = Sequential()
model.add(Input(shape = (None,4800)))
model.add(Dense(num_classes, activation=ACTIVATION))
model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
model.fit(x_train_skipthought, yt, epochs=EPOCHS)
print('Test accuracy:', model.evaluate(x_test_skipthought, yte)[1])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: model.py <vectors_file> <training_data> <test_data>')
        exit(-1)
    else:
        embeddings_index = loadVectors(sys.argv[1])
        x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, num_classes = loadData(sys.argv[2], sys.argv[3], embeddings_index)
    print("Glove Based model")
    create_and_model(x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, EMBEDDING_DIM, num_classes)
    print("OneHot Based Model")
    create_and_model(x_test, x_train, x_val, y_test, y_train, y_val,num_words, '', num_words, num_classes)