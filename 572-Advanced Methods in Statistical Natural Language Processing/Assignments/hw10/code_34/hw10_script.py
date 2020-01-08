#!/usr/bin/env python2
"""Neural net training & testing code for LING 572 HW 10 
USAGE: python hw10_script.py config_file""" 


import network
import newsgroup_loader
import numpy as np
import sys
import yaml

if __name__ == "__main__":
    # Open the config file and get the hyperparameter values 
    config_file = sys.argv[1]
    with open(config_file, 'r') as ymlfile:
        config = yaml.load(ymlfile)
    MAX_FEATURES = int(config['input_shape'])
    OUTPUT_SHAPE = int(config['output_shape'] )
    LAYERS = int(config['hidden_layers'])
    if LAYERS > 1:
        HIDDEN_NEURONS = [int(n) for n in config['hidden_neurons'].split()]
    else:
        HIDDEN_NEURONS = int(config['hidden_neurons'])
    EPOCHS = int(config['epochs'])
    BATCH_SIZE = int(config['batch_size'] )
    LEARNING_RATE = float(config['learning_rate'])
    ACTIVATION = int(config['activation'])

    # The document categories of interest
    categories =\
        ['talk.politics.guns','talk.politics.mideast', 'talk.politics.misc']
       
    # Load train & test data from those categories
    train_data, test_data = newsgroup_loader.load_data(categories, MAX_FEATURES)
    
    if LAYERS == 1:
        layer_sizes = [MAX_FEATURES, HIDDEN_NEURONS, OUTPUT_SHAPE]
    # Unattractive way of creating the first argument to the network:
    else:
        layer_sizes = [MAX_FEATURES]
        layer_sizes.extend(HIDDEN_NEURONS)
        layer_sizes.append(OUTPUT_SHAPE)

    # Build a neural network with the architecture and activation
    # specified in the config file
    net = network.Network(layer_sizes, activation=ACTIVATION)
    # Train and test the network using hyperparameters from config file
    net.SGD(train_data, EPOCHS, BATCH_SIZE, LEARNING_RATE, test_data=test_data)
