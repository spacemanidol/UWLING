# ATIS Intent Classifier
For this homework the task was to create a NN classifier in keras to perform intent prediction on the ATIS dataset. 
## Usage
Model is mostly self contained. As long as you provide the training and test data and a glove style vector file the command below will handle the rest
'''
python model.py ../vectors.txt atis.train.w-intent.IOB atis.test.w-intent.IOB
'''
## Implementation
My model does the following
* loads previously create glove vectors. 
* loads the data, ignore the tags, tokenize the text it and converts the target labels(ys) to ints for easy management(If any class has more than one correct intent then I assume the first intent is the correct one). For all intents in test set not present in the train dataset I assign an new class for which my model can never predict correctly. 
* split the data into a cross validated dev set. I do this to iterate and understand model accuracy without touching the test set.  
* create an embedding matrix and a one-hot matrix to represent all the words in the training data. 
* build out the Neural Networks(CNN and pooling and Bidirectional LSTMSDescribed below) with two forms of text represenation, one-hot and embedding based.
* train the model and evaluate performance on held out data.

## Network/ Model Structure
For the network I tried various NN structures and tweaked based on what I saw got better accuracy. 
Initially, I started with a convolution layer and a pooling layer which I used to pick various of my hyper parameters. 
Various experiments in # of layers, actiation functions, optizer, etc had me top out accuracy at ~72% for both word represeantion methods.
Seeing this I decided to try another model type and I tried out a Bidirectional LSTM. I found that after some model tweaking I could produce similair accuracy to the Convolutional network but much slower to train.

My parameters were based on training time and optimal accuracy. I mostly focused on model architecture and the # of hidden neurons.   
## HyperParameters (BEST RESULTS)
Optimizer:rmsprop (This optimizer tended to learn way faster)
Epochs:20 (Seemed to be the threshold when accuracy stopped improving)
Batch Size:128 (Any smaller seemed to make training too time consuming)
Hidden Neurons: 32 (I experimented with 8, 32, 64, 128)
Loss Function:categorical_crossentropy
Validation Split: 0.1
Dropout:0.5
Activation: RELU
Final Activation: sigmoid (Seemd to consistently produce 2% higher accuracy scores)

## Results
CNN Model OneHot
-8 Hidden Neurons Per layer: 0.722284434423735
-32 Hidden Neurons Per layer: 0.7211646135950676
-64 Hidden Neurons Per layer: 0.7178051524439958
-128 Hidden Neurons Per layer: 0.6987681982899032
CNN Model Embedding
-8 Hidden Neurons Per layer: 0.722284434423735
-32 Hidden Neurons Per layer: 0.7323628218817417
-64 Hidden Neurons Per layer: 0.708846584479726
-128 Hidden Neurons Per layer: 0.6875699874001148
Bidirectional LSTMS OneHot
-8 Hidden Neurons Per layer: 0.722284434423735
-32 Hidden Neurons Per layer: 0.7021276581060446
-64 Hidden Neurons Per layer: 0.6528555442477928
-128 Hidden Neurons Per layer: 0.6328555442477928
Bidirectional LSTMS Embedding
-8 Hidden Neurons Per layer: 0.722284434423735
-32 Hidden Neurons Per layer: 0.7021276581060446
-64 Hidden Neurons Per layer: 0.7000447927664002
-128 Hidden Neurons Per layer: 0.6987681982899032

## Analysis 
In general I found that after 32 hidden neurons, adding more did not make the model more accurate. I also found that in general the embedding model performs slightly better than onehat.
Where there is a bigger difference is the learning speed. The embedding based model is able to have a high accuracy(~60) within the first epoch while the onehot model takes ~3 epochs to reach the same accuracy.
In general, it seems that a OneHot model require more 'learning' to approximate the represenation that the embedding model can offer. Additionally, since my onehot model had
## Other notes
While exploring models I learned that Keras function for evaluate is a little bit finiky. If you are doing a categorical network(aka clasification like ATIS) you cannot use accuracy as a metric and must use categorical_accuracy. 
Initially I was not doing this and all model were gettin ~96% accuracy, which when computed out of keras, the accuracy was ~40%