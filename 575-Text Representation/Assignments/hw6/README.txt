# Averaged Word Vectors VS Skipthought

## Implementation
My model does the following
* loads previously create Word2Vec embedding
* loads the data, ignore the tags, tokenize the text it and converts the target labels(ys) to ints for easy management(If any class has more than one correct intent then I assume the first intent is the correct one). 
* create an embedding matrix and a one-hot matrix to represent all the words in the training data. 
* Train various forms of word embedding with land evaluate with a simple logistic logistic regression

## HyperParameters 
Vectors:Negative Sampling Skip Gram (200D)
Optimizer:rmsprop
Epochs:20 
Loss Function:categorical_crossentropy
Activation: softmax

## Results
In the methods below I refer to sentence 1 as v and sentence 2 as u. All methods are pairwise methods.
Skipthought: 0.858463714763
Averaged Word Embedding(Just concatenating Sentence1 and Sentence2):0.6105134971175205
Average Word Embedding(np.abs(v - u), v * u) :0.733306271565
Average Word Embedding(v, u np.abs(v - u), v * u) :0.7124010552275076
Average Word Embedding(v, u np.abs(v - u), v + u, v * u) :0.7124010552275076
Average Word Embedding(v, u v + u, v * u) :0.678100263682877

## Usage
'''
python model.py ../vectors.txt SICK_train.txt SICK_test_annotated.txt
'''

## Analysis
For this experiment I decided I would explore various sentence representation methods to better understand how word vectors can represent a sentence.
Looking at thew results its clear that skipthought vectors outperform all other methods by a fair amount. 
Its also worth noting that in almost every case(except averaged word embedding) the skipthought model had less dimensions so could train quicker.
With my other experiments I found that averaged word embedding are not the most optimal form of sentence representation but perhaps the easiest and quickest.
During some debugging of my losses I found the dataset contained many OOV terms and thus a lot of important terms could not be learned by the network.
Its worth noting that the Averaged word embedding inspired by conneau et al. that I implemented start to get performance that approximates skipthoughts but the vector size has quickly grown to 20,000.

It seems that as long as your project does not need to be fast with the encoding of sentence vectors(it was the slowest part of the implementation) choosing to use a sentence representation can be a great idea.