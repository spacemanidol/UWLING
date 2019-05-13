import os
import sys
import math
import numpy as np

from keras.preprocessing.text import Tokenizer, one_hot
from keras import backend as K
from keras.preprocessing.sequence import pad_sequences
from keras.initializers import Constant
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Input, Embedding, Lambda
from sklearn.utils import column_or_1d

EPOCHS = 20
EMBEDDING_DIM = 200
MAX_SEQUENCE_LENGTH = 20
MAX_NUM_WORDS = 400000
OPTIMIZER = 'rmsprop'
ACTIVATION = 'softmax'
LOSSFUNCTION = 'categorical_crossentropy'

def make2D(source, embedding_matrix):
    target = np.zeros((len(source), MAX_SEQUENCE_LENGTH * EMBEDDING_DIM))
    for i in range(len(source)):  
        for j in range(1,MAX_SEQUENCE_LENGTH):
            vect = embedding_matrix[source[i][j]]
            for k in range(EMBEDDING_DIM):
                t = j*EMBEDDING_DIM + k
                target[i][t] = vect[k] 
    return target

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

def runCombo(train, test, y_train, y_test, num_classes):
    model = Sequential()
    model.add(Dense(num_classes,input_shape=train[0].shape, activation='softmax'))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(train, y_train, epochs=EPOCHS)
    return model.evaluate(test, y_test)[1]

def loadandRunData(embeddings_index, train_data_filename, test_data_filename):
    embeddings_index_len = len(embeddings_index)
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    x_train, y_train, x_test, y_test = [], [], [], []
    u_train, u_test, v_train, v_test = [], [], [], []
    with open(train_data_filename, 'r') as f:
        f.readline()# header
        for l in f:
            l = l.strip().split('\t')
            u_train.append(l[1])
            v_train.append(l[2])
            x_train.append(' '.join(l[1:3]))
            y_train.append(l[4])

    with open(test_data_filename,'r') as f:
        f.readline()# header
        for l in f:
            l = l.strip().split('\t')
            u_test.append(l[1])
            v_test.append(l[2])
            x_test.append(' '.join(l[1:3]))
            y_test.append(l[4])

    all_classes = list(set(y_train))
    num_classes = len(all_classes) + 1
    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
    embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        if i > MAX_NUM_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=MAX_SEQUENCE_LENGTH)
    x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=MAX_SEQUENCE_LENGTH)
    u_train = pad_sequences(tokenizer.texts_to_sequences(u_train), maxlen=MAX_SEQUENCE_LENGTH)
    u_test = pad_sequences(tokenizer.texts_to_sequences(u_test), maxlen=MAX_SEQUENCE_LENGTH)
    v_train = pad_sequences(tokenizer.texts_to_sequences(v_train), maxlen=MAX_SEQUENCE_LENGTH)
    v_test = pad_sequences(tokenizer.texts_to_sequences(v_test), maxlen=MAX_SEQUENCE_LENGTH)
    y_train = to_categorical(np.asarray(transform(np.array(all_classes), y_train)), num_classes=num_classes)
    y_test = to_categorical(np.asarray(transform(np.array(all_classes), y_test)), num_classes=num_classes)
    v_test = make2D(v_test, embedding_matrix)
    v_train = make2D(v_train, embedding_matrix)
    u_test = make2D(u_test, embedding_matrix)
    u_train = make2D(u_train, embedding_matrix)
    model = Sequential()
    model.add(Embedding(num_words,  EMBEDDING_DIM, weights=[embedding_matrix], trainable=True))
    model.add(Lambda(function=lambda x: (K.sum(x, axis=1))/math.sqrt(MAX_SEQUENCE_LENGTH), output_shape=lambda shape: (shape[0],) + shape[2:]))
    model.add(Dense(num_classes, activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(x_train, y_train, epochs=EPOCHS)
    print('Test accuracy average of word embeddings u and v:', model.evaluate(x_test, y_test)[1])
    test = np.c_[np.abs(v_test - u_test), v_test * u_test]
    train = np.c_[np.abs(v_train - u_train), v_train * u_train]
    print('Test accuracy on abs(v-u),U*V:{}'.format(runCombo(train,test,y_train,y_test, num_classes)))
    test = np.c_[v_test, u_test, np.abs(v_test - u_test), v_test * u_test]
    train = np.c_[v_train, u_train, np.abs(v_train - u_train), v_train * u_train]
    print('Test accuracy on v,u, abs(v-u),U*V:{}'.format(runCombo(train,test,y_train,y_test, num_classes)))
    test = np.c_[v_test, u_test, v_test + u_test, v_test * u_test]
    train = np.c_[v_train, u_train, v_train + u_train, v_train * u_train]
    print('Test accuracy on v,u, v+u,U*V:{}'.format(runCombo(train,test,y_train,y_test, num_classes)))
    test = np.c_[v_test, u_test, np.abs(v_test - u_test),v_test+u_test, v_test * u_test]
    train = np.c_[v_train, u_train, np.abs(v_train - u_train),v_train+u_train, v_train * u_train]
    print('Test accuracy on v,u,v+u, abs(v-u),U*V:{}'.format(runCombo(train,test,y_train,y_test, num_classes)))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: model.py <vectors_file> <training_data> <test_data>')
        exit(-1)
    else:
        embeddings_index = loadVectors(sys.argv[1])
        loadandRunData(embeddings_index, sys.argv[2], sys.argv[3])