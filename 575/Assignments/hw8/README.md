
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
pip install numpy theano nose scipy pytorch-pretrained-bert torch
#wget condprobs will go here
'''

### generate condprobs
'''
python generate_pairs.py <min_count> <window_size>
touch probs
python generate_cond_probs.py probs pairs
'''

### generate embeddings
'''
generate_embedding.py text 20 3 probs 50 20-3-50.pkl
'''

### Evaluate
'''
python evaluate.py 20-3-50.pkl wordsim353.txt Simlex999.txt MEN3k.txt
python evaluate.py LM-20-3-50.pkl wordsim353.txt Simlex999.txt MEN3k.txt
'''

### Results
Window size = 3, Min count = 20

Window size = 5, Min count = 20

Window size = 10, Min count = 20

Window size = 3, Min count = 10

Window size = 5, Min count = 10

Window size = 10, Min count = 10

Window size = 3, Min count = 5

Window size = 5, Min count = 5

Window size = 10, Min count = 5



