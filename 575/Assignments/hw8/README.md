
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
|Benchmark |Regular Glove|LME(e^P(Y\|X)) |LME(e^(P(Y\|X)+P(X\|Y))|LME(2e^(P(Y\|X)+P(X\|Y))|LME(2^e^(P(Y\|X)+P(X\|Y))|LME(e^e^(P(Y\|X)+P(X|\Y))|
|----------|-------------|--------------|---------------------|----------------------|-----------------------|-----------------------|
|MEN3K     |0.3144       |0.3206(1.97%) |0.3214(2.22%)        |0.3445(9.58%)         |0.3489(10.99%)         |0.3602(14.57%)         |
|Simlex999 |0.1465       |0.1452(-0.85%)|0.1368(-6.60%)       |0.1537(4.94%)         |0.1602(9.40%)          |0.1584(8.15%)          |
|wordsim353|0.3840       |0.3961(3.17%) |0.3932(2.41%)        |0.4095(6.64%)         |0.4137(7.74%)          |0.4036(5.10%)          |
|Average   |0.2816       |0.2873(2.03%) |0.2838(0.77%)        |0.3026(7.44%)         |0.3076(9.24%)          |0.3074(9.15%)          |

##### Modifying the cooccurrence matrix
For this next experiment we ste away from the concept of updating the cooccurrence model with just setting the cooccurrence matrix to the probability. We only update occurences that happen in the text. All others are set to 0
|Benchmark |Regular Glove |e^1            |e^e^(P(Y\|X)+P(X\|Y)|1              |P(Y\|X)+P(X\|Y)|
|----------|--------------|---------------|--------------------|---------------|---------------|
|MEN3K     |0.3144        |0.1761(-43.98%)|0.1758(-44.08%)     |0.0532(-83.08%)|0.0499(-84.13%)|
|Simlex999 |0.1465        |0.1243(-15.13%)    |0.1243(-15.13%)     |0.0368(-74.89%)|0.0335(-77.14%)|
|wordsim353|0.3840        |0.1322(-65.57%)|0.1898(-50.57%)     |0.0330(-91.42%)|0.0404(-89.48%)|
|Average   |0.2816        |0.1615(-42.66%)|0.1633(-42.01%)     |0.0401(-85.45%)|0.0413(-85.35%)|

#### Reuters Document Classification Training set size
To explore the effects of these LME embeddings we created a logistic regression classifier for the document
|WordVector|15 Samples|147 Samples|221 Samples|265 Samples|294 Samples|441 Samples|
|Glove     |0.0006    |0.0585     |0.2745     |0.3093     |0.9463     |1.000      |
|LME       |0.0074    |0.1823     |0.9940     |0.8809     |1.0000     |1.000      |