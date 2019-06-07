
### Prep the env
'''
LAMBDA_REPO=$(mktemp) && \
wget -O${LAMBDA_REPO} https://lambdalabs.com/static/misc/lambda-stack-repo.deb && \
sudo dpkg -i ${LAMBDA_REPO} && rm -f ${LAMBDA_REPO} && \
sudo apt-get update && sudo apt-get install -y lambda-stack-cuda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
wget http://mattmahoney.net/dc/enwik8.zip
unzip enwik8.zip
sudo reboot
conda create -n hw8 python=3
conda activate hw8
#wget condprobs will go here
'''

### generate condprobs
'''
python generate_pairs.py <min_count> <window_size>
touch probs
python generate_cond_probs.py probs pairs
'''

### Test
'''
python evaluate.py 20-3-50.pkl wordsim353.txt Simlex999.txt MEN3k.txt
python evaluate.py LM-20-3-50.pkl wordsim353.txt Simlex999.txt MEN3k.txt
'''

### Results
All word vectors were trained for 25 iterations with a window size of 10, mincount = 1 and creating 100 dimensional vectors
#### Word Similairty Experiments
##### Modifying the increment
For the first experiment we tune the cooccurence matrix update increment
LM Enhanced Glove(LME) 
|Benchmark |Regular Glove |LME(e^P(Y|X)) |LME(e^(P(Y|X)+P(X|Y))|LME(2e^(P(Y|X)+P(X|Y))|LME(2^e^(P(Y|X)+P(X|Y))|LME(e^e^(P(Y|X)+P(X|Y))|
|----------|--------------|--------------|---------------------|----------------------|-----------------------|-----------------------|
|MEN3K     |0.314398152589|0.320601183731|0.321377026371       |0.344519329357        |0.348937699361         |0.360218696733         |
|Simlex999 |0.146473433053|0.145232696260|0.136800090145       |0.153712677209        |0.160236075104         |0.158407798893         |
|wordsim353|0.383981074929|0.396164335267|0.393222707322       |0.409482356739        |0.413712964303         |0.403561084199         |
|Average   |0.281617553524|0.287332738419|0.2837999412         |0.302571454435        |0.307628912923         |30739585994167         |

##### Modifying the cooccurrence matrix
For this next experiment we ste away from the concept of updating the cooccurrence model with just setting the cooccurrence matrix to the probability. We only update occurences that happen in the text. All others are set to 0
|Benchmark |Regular Glove |e^1           |e^e^(P(Y|X)+P(X|Y)|1              |P(Y|X)+P(X|Y)  |
|----------|--------------|--------------|------------------|---------------|---------------|
|MEN3K     |0.314398152589|0.176114491485|0.175812288377    |0.0531827480081|0.0499039256198|
|Simlex999 |0.146473433053|0.176114491485|0.124307150217    |0.0367767460488|0.0334854769477|
|wordsim353|0.383981074929|0.132186760754|0.189789158249    |0.0329525451829|0.0404052431466|
|Average   |0.281617553524|
#### Reuters Document Classification Training set size

15/15 [==============================] - 0s - loss: 4.5326 - categorical_accuracy: 0.0000e+00
6240/6910 [==========================>...] - ETA: 0sTest accuracy: [4.4548754863214564, 0.00057887120115774238]
LM Based
15 new size x_Train

15/15 [==============================] - 0s - loss: 4.4709 - categorical_accuracy: 0.0000e+00
6208/6910 [=========================>....] - ETA: 0sTest accuracy: [4.4256765756179215, 0.0073806078147612159]


221/221 [==============================] - 0s - loss: 4.2243 - categorical_accuracy: 0.0633
6208/6910 [=========================>....] - ETA: 0sTest accuracy: [4.0908082933053267, 0.27452966715337224]
LM Based
221 new size x_Train

221/221 [==============================] - 0s - loss: 4.0637 - categorical_accuracy: 0.4932
6464/6910 [===========================>..] - ETA: 0sTest accuracy: [3.9263263916313735, 0.99406657018813316]


265/265 [==============================] - 0s - loss: 4.3387 - categorical_accuracy: 0.0264
6240/6910 [==========================>...] - ETA: 0sTest accuracy: [4.1700927037406075, 0.30926193927890483]
LM Based
265 new size x_Train

265/265 [==============================] - 0s - loss: 4.1595 - categorical_accuracy: 0.1170
6240/6910 [==========================>...] - ETA: 0sTest accuracy: [4.0042106716746702, 0.8808972504135496]

1% data
147/147 [==============================] - 0s - loss: 4.3422 - categorical_accuracy: 0.0000e+00
6336/6910 [==========================>...] - ETA: 0sTest accuracy: [4.2242477498420241, 0.058465991324479605]
LM Based
147 new size x_Train

147/147 [==============================] - 0s - loss: 4.3124 - categorical_accuracy: 0.0408
6208/6910 [=========================>....] - ETA: 0sTest accuracy: [4.2048449830967511, 0.18234442839487935]

2% 

294/294 [==============================] - 0s - loss: 4.2422 - categorical_accuracy: 0.1497
6910/6910 [==============================] - 0s
Test accuracy: [4.0687619229991601, 0.94630969597185743]
LM Based
294 new size x_Train

294/294 [==============================] - 0s - loss: 4.1584 - categorical_accuracy: 0.4592
6880/6910 [============================>.] - ETA: 0sTest accuracy: [3.9825710923902897, 1.0]

3%

441/441 [==============================] - 0s - loss: 4.0982 - categorical_accuracy: 0.6236
6176/6910 [=========================>....] - ETA: 0sTest accuracy: [3.9022197526029152, 1.0]
LM Based
441 new size x_Train

441/441 [==============================] - 0s - loss: 4.0039 - categorical_accuracy: 0.4966 

4%

587/587 [==============================] - 0s - loss: 4.1186 - categorical_accuracy: 0.4174
6784/6910 [============================>.] - ETA: 0sTest accuracy: [3.861085835759098, 1.0]
LM Based
587 new size x_Train

587/587 [==============================] - 0s - loss: 4.1944 - categorical_accuracy: 0.2641
6910/6910 [==============================] - 0s
Test accuracy: [3.953612598565484, 0.98885672937771341]

5% Data

734/734 [==============================] - 0s - loss: 3.9731 - categorical_accuracy: 0.8052
6784/6910 [============================>.] - ETA: 0sTest accuracy: [3.687804863663382, 1.0]
LM Based
734 new size x_Train

734/734 [==============================] - 0s - loss: 3.9848 - categorical_accuracy: 0.7629
6880/6910 [============================>.] - ETA: 0sTest accuracy: [3.6901447657048272, 1.0]





