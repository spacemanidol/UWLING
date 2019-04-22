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

BATCH_SIZE = 128
EPOCHS = 5
EMBEDDING_DIM = 200
HIDDEN_DIM = 64
POOLING_DIM = 5
MAX_SEQUENCE_LENGTH = 100
MAX_NUM_WORDS = 200000
VALIDATION_SPLIT = 0.1
DROPOUT = 0.3
OPTIMIZER = 'rmsprop'
ACTIVATION = 'sigmoid'
LOSSFUNCTION = 'categorical_crossentropy'

def loadVectors(filename):
    print('Indexing word vectors.')
    embeddings_index = {}
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            embeddings_index[l[0]] = np.array([float(i) for i in l[1:]])
    print('Found %s word vectors.' % len(embeddings_index))
    return embeddings_index

def loadData(train_data_filename, test_data_filename, embeddings_index):
    embeddings_index_len = len(embeddings_index)
    print('Processing train dataset')
    texts, labels, label2idx, int_labels = [], [], {}, []
    idx = 0
    with open(train_data_filename, encoding='latin-1') as f:
        for l in f:
            l = l.strip().split('\t')
            texts.append(l[0])
            labels.append(l[1].split(' ')[-1].split('#')[0]) # for any class that has multiple lables we take just the first
    allLabels = set(labels)
    for label in allLabels:
        label2idx[label] = idx
        idx += 1
    for label in labels:
        int_labels.append(label2idx[label])
    labels = int_labels
    print('Found %s training examples.' % len(texts))
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    word_index = tokenizer.word_index
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    labels = to_categorical(np.asarray(labels))
    print('Found %s unique tokens.' % len(word_index))
    print('Shape of data tensor:', data.shape)
    # split the data into a training set and a validation set
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]
    num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])
    x_train = data[:-num_validation_samples]
    y_train = labels[:-num_validation_samples]
    x_val = data[-num_validation_samples:]
    y_val = labels[-num_validation_samples:]
    print('Preparing embedding matrix and One-Hot Matrix')
    num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
    embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
    one_hot_matrix =  np.zeros((num_words, num_words))
    for word, i in word_index.items():
        if i > MAX_NUM_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        one_hot_matrix[i][one_hot(word, num_words)] = 1
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    print('Processing test dataset')
    texts, labels = [], []
    with open(test_data_filename, encoding='latin-1') as f:
        for l in f:
            l = l.strip().split('\t')
            texts.append(l[0])
            labels.append(l[1].split(' ')[-1].split('#')[0]) # for any class that has multiple lables we take just the first
    int_labels = []
    for label in labels:
        if label not in label2idx:
            int_labels.append(-1)
        else:
            int_labels.append(label2idx[label])
    labels = int_labels
    print('Found %s test examples.' % len(texts))
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    x_test = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    y_test = to_categorical(np.asarray(labels))
    return x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, one_hot_matrix, len(allLabels)

def create_and_model(x_test, x_train, x_val, y_test, y_train, y_val, num_words, embedding_matrix, embedding_dim, label_len):
    ##Convolution and pooling
    print('Training Convolutional model.')
    model = Sequential()
    model.add(Embedding(num_words,  embedding_dim, embeddings_initializer=Constant(embedding_matrix), input_length=MAX_SEQUENCE_LENGTH, trainable=False))
    model.add(Conv1D(HIDDEN_DIM, 5, activation='relu'))
    model.add(Dropout(DROPOUT))
    model.add(MaxPooling1D(5))
    model.add(Conv1D(HIDDEN_DIM, 5, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dropout(DROPOUT))
    model.add(Dense(label_len, activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_val, y_val))
    #model.summary()
    print('Test accuracy:', model.evaluate(x_test, y_test, batch_size=BATCH_SIZE, verbose=1)[1])
    print('Training BiLSTM model.')
    ## Bidirectional stacked LSTM
    model = Sequential()
    model.add(Embedding(num_words,  embedding_dim, embeddings_initializer=Constant(embedding_matrix), input_length=MAX_SEQUENCE_LENGTH, trainable=False))
    model.add(Bidirectional(LSTM(HIDDEN_DIM, return_sequences=True)))
    model.add(AttentionWithContext())
    model.add(Dropout(DROPOUT))
    model.add(Bidirectional(LSTM(HIDDEN_DIM, return_sequences=True)))
    model.add(AttentionWithContext())
    model.add(Dropout(DROPOUT))
    model.add(Bidirectional(LSTM(HIDDEN_DIM)))
    model.add(Dropout(DROPOUT))
    model.add(Dense(label_len, activation=ACTIVATION))
    model.compile(optimizer=OPTIMIZER, loss=LOSSFUNCTION, metrics=['categorical_accuracy'])
    model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(x_val, y_val))
    #model.summary()
    print('Test accuracy:', model.evaluate(x_test, y_test, batch_size=BATCH_SIZE, verbose=1)[1])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: model.py <vectors_file> <training_data> <test_data>')
        exit(-1)
    else:
        embeddings_index = loadVectors(sys.argv[1])
        x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, one_hot_matrix, label_len = loadData(sys.argv[2], sys.argv[3], embeddings_index)
    print("Glove Based model")
    create_and_model(x_test, x_train, x_val, y_test, y_train, y_val,num_words, embedding_matrix, EMBEDDING_DIM, label_len)
    print("OneHot Based Model")
    create_and_model(x_test, x_train, x_val, y_test, y_train, y_val,num_words, one_hot_matrix, num_words, label_len)