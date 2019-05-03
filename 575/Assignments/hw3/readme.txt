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
## HyperParameters 
Optimizer:rmsprop (This optimizer tended to learn way faster)
Epochs:20 
Hidden Neurons: 32 (I experimented with 32,64,128,256)
Loss Function:categorical_crossentropy
Validation Split: 0.01 (Just to confirm when models collapse)
Dropout:0.4
Activation: RELU
Final Activation: softmax

## Results
CNN Model OneHot: 0.8185890264900908
CNN Model Embedding: 0.8432250839865622
Bidirectional LSTMS OneHot: 0.7715565510853407
Bidirectional LSTMS Embedding: 0.7861142225922289

Its worth noting that the performance on the dev set would swing +=10% run to run but the performance ratios were pretty consistent with above. Though Onehot approximates embedding based it usually takes much larger to reach the same accuracy. 
