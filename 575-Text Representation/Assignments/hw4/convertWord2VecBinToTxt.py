import sys
from gensim.models.keyedvectors import KeyedVectors
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: convertWord2VecBinToTxt.py <vectors_file> <target_name>')
        exit(-1)
    else:
        KeyedVectors.load_word2vec_format(sys.argv[1],binary=True).save_word2vec_format(sys.argv[2],binary=False)