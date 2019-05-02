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
After I had Finished building my initial network I found that my code had bugs in the loading of the target data which kept my NNs from learning the task as well. 
I have since updated the networks.
The experiment contains a CNN and a BiLSTM which run with onehot and trained word embedding.

My parameters were based on training time and optimal accuracy.
## HyperParameters (BEST RESULTS)
Optimizer:rmsprop (This optimizer tended to learn way faster)
Epochs:10 (CNNs seem to find false minimas after 10 steps)
Hidden Neurons: 200 (I experimented with 10, 50, 100, 200)
Loss Function:categorical_crossentropy
Validation Split: 0.01 (Just to confirm when models collapse)
Dropout:0.4
Activation: RELU
Final Activation: sofrmax (Seemd to consistently produce 10% higher accuracy scores vs sigmoid)

## Results
CNN Model OneHot
-10 Hidden Neurons Per layer: 
-50 Hidden Neurons Per layer: 
-100 Hidden Neurons Per layer: 
-200 Hidden Neurons Per layer: 0.7905935053061798
CNN Model Embedding
-10 Hidden Neurons Per layer: 
-50 Hidden Neurons Per layer: 
-100 Hidden Neurons Per layer: 
-200 Hidden Neurons Per layer:  0.8085106378306467
Bidirectional LSTMS OneHot
-10 Hidden Neurons Per layer: 
-50 Hidden Neurons Per layer: 
-100 Hidden Neurons Per layer: 
-200 Hidden Neurons Per layer: 0.7905935053061798
Bidirectional LSTMS Embedding
-10 Hidden Neurons Per layer: 
-50 Hidden Neurons Per layer: 
-100 Hidden Neurons Per layer: 
-200 Hidden Neurons Per layer: 0.8085106378306467
## Analysis 
In general I found that after 32 hidden neurons, adding more did not make the model more accurate. I also found that in general the embedding model performs slightly better than onehat.
Where there is a bigger difference is the learning speed. The embedding based model is able to have a high accuracy(~60) within the first epoch while the onehot model takes ~3 epochs to reach the same accuracy.
In general, it seems that a OneHot model require more 'learning' to approximate the represenation that the embedding model can offer. Additionally, since my onehot model had
## Other notes
While exploring models I learned that Keras function for evaluate is a little bit finiky. If you are doing a categorical network(aka clasification like ATIS) you cannot use accuracy as a metric and must use categorical_accuracy. 
Initially I was not doing this and all model were gettin ~96% accuracy, which when computed out of keras, the accuracy was ~40%