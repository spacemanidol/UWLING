from __future__ import print_function

import os
import sys
import numpy as np

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Input, GlobalMaxPooling1D, MaxPooling1D, Embedding, Conv1D, LSTM, Bidirectional
from sklearn.utils import column_or_1d

EPOCHS = 20
EMBEDDING_DIM = 200
HIDDEN_DIM = 256
POOLING_DIM = 5
MAX_SEQUENCE_LENGTH = 50
MAX_NUM_WORDS = 400000
VALIDATION_SPLIT = 0.01
DROPOUT = 0.2
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

def loadData(train_data_filename, test_data_filename, embeddings_index):
    embeddings_index_len = len(embeddings_index)
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    x_train, y_train, x_test, y_test = [], [], [], []
    with open(train_data_filename, encoding='latin-1') as f:
        for l in f:
            l = l.strip().split('\t')
            x_train.append(l[0])
            y_train.append(l[1].split(' ')[-1])
    with open(test_data_filename, encoding='latin-1') as f:
        for l in f:
            l = l.strip().split('\t')
            x_test.append(l[0])
            y_test.append(l[1].split(' ')[-1])
    all_classes = list(set(y_train))
    num_classes = len(all_classes) + 1
    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=MAX_SEQUENCE_LENGTH)
    x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=MAX_SEQUENCE_LENGTH)
    y_train = to_categorical(np.asarray(transform(np.array(all_classes), y_train)), num_classes=num_classes)
    y_test = to_categorical(np.asarray(transform(np.array(all_classes), y_test)), num_classes=num_classes)
    indices = np.arange(x_train.shape[0])
    num_validation_samples = int(VALIDATION_SPLIT * x_train.shape[0])
    np.random.shuffle(indices)
    x_train= x_train[indices]
    y_train = y_train[indices]
    x_val = x_train[-num_validation_samples:]
    x_train = x_train[:-num_validation_samples]
    y_val = y_train[-num_validation_samples:]
    y_train = y_train[:-num_validation_samples]
    num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
    embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > MAX_NUM_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, num_classes

def create_and_model(x_test, x_train, x_val, y_test, y_train, y_val, num_words, embedding_matrix, embedding_dim, num_classes):
    embedding_layer = Embedding(num_words,  embedding_dim)
    if len(embedding_matrix) > 0:
        Embedding(num_words,  embedding_dim, weights=[embedding_matrix], trainable=True)
    model = Sequential()
    model.add(embedding_layer)
    model.add(Dropout(DROPOUT))
    model.add(Conv1D(HIDDEN_DIM, POOLING_DIM, activation='relu'))
    model.add(Dropout(DROPOUT))
    model.add(MaxPooling1D(POOLING_DIM))
    model.add(Conv1D(HIDDEN_DIM, POOLING_DIM, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(num_classes, activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=EPOCHS)
    print('Test accuracy:', model.evaluate(x_test, y_test)[1])
    model = Sequential()
    model.add(embedding_layer)
    model.add(Dropout(DROPOUT))
    model.add(Bidirectional(LSTM(HIDDEN_DIM, return_sequences=False)))
    model.add(Dense(num_classes, activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    #model.fit(x_train, y_train,  epochs=EPOCHS, validation_data=(x_val, y_val))
    #print('Test accuracy:', model.evaluate(x_test, y_test)[1])

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
    #create_and_model(x_test, x_train, x_val, y_test, y_train, y_val,num_words, '', num_words, num_classes)