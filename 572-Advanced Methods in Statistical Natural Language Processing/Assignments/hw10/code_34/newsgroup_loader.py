#!/usr/bin/env python2
"""20newsgroups corpus data loader.
Uses TfidfVectorizer to preprocess the data and reshapes the input and output
for use in the network training and testing code."""


import numpy as np

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorized_result(i, size):
    """Return one-hot encoded vector given an int, i"""
    e = np.zeros((size, 1))
    e[i] = 1.0
    return e

def load_data(categories, max_features):
    """Load data from 20newsgroups corpus from given list of categories.
    Return Tfidf vectorized train and test data."""
    train = fetch_20newsgroups(subset='train', categories=categories)
    test = fetch_20newsgroups(subset='test', categories=categories)
   
    # The train labels need to be vectorized for training 
    train_labels = [vectorized_result(y, len(categories)) for y in train.target]
    # The test labels do not.
    test_labels = test.target    

    # Vectorize the data using Tfidf fit on the training data
    vectorizer = TfidfVectorizer(max_features=max_features)
    train_vectors = vectorizer.fit_transform(train.data)
    test_vectors = vectorizer.transform(test.data)

    # Prepare lists of inputs
    train_inputs = [np.array(x.T) for x in train_vectors.todense()]
    test_inputs = [x.T for x in test_vectors.todense()]

    # Zip the inputs and the labels 
    train_data = zip(train_inputs, train_labels)
    test_data = zip(test_inputs, test.target)
    
    return train_data, test_data
