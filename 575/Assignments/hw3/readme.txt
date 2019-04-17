# ATIS Intent Classifier
For this homework the task was to create a NN classifier in keras to perform intent prediction on the ATIS dataset. 
## Usage
Model is mostly self contained. As long as you provide the training and test data and a glove style vector file the command below will handle the rest
'''
python model.py ../vectors.txt atis.train.w-intent.IOB atis.test.w-intent.IOB
'''
## Implementation
First, my implementation loads previously create glove vectors. Second, the model loads the data, tokenizes it and converts the target labels(ys) to ints for easy management. If any class has more than one correct intent then I assume the first intent is the correct one. Additionally, for all intents not present in the train dataset I assign an new class for which my model can never predict correctly. 
Next, the model loads the data and using the loaded embeddings creates an embedding matrix and a one-hot matrix to represent all the words in the training data. After that, the model creates two neural net(one for glove represenation, one for onehot) which it trains and evaluates on.

## Network
For my network I thought given the relative simplicit of this task a CNN would likley be the best fit so first off I made a simple CNN with 4 Convolutional layers and 128 hidden units. Seeing this was slow but accurate I kept on tweaking the size and layers until I made the model small and fast but kept high accuracy. The final model has 2 convolution laters with 8 hidden neurons. Once I had a performat and accurate model I started doing a hyperparameter sweep to make sure I couldn't improve. Of all the hyperparameters the most effective in changing model accuracy is the optimizer and the loss function. By changing the loss function from Mean Squared Error to Binary Crossentropy the model accuracy imrpoves from ~2% to 70% and from 70% to 85% for Glove based and One-HoT based methods respectively. By switching from SGD to rms prop model accuracy imrpoves from ~70% to 95% and from 85% to 96% for Glove based and OneHAT based methods respectively. Some smaller optimizations were sigmoid vs softmax(~2% accuracy gain by using sigmoid)
## HyperParameters
After various tunning experiments I chose the following HyperParameters
Optimizer:rmsprop
Epochs:3
Batch Size:64
Hidden Neurons: 8
Convoltions: 2
Loss Function:binary_crossentropy
Dropout:0.1
Activation: RELU
Final Activation: Sigmoid

## One-Hot vs Glove
During my experiment I found that in larger and more complex networks Glove performance tended to beat one-hot but as I made my network smaller model accuracy seems to equalize and one-hot seemled to learn faster.


