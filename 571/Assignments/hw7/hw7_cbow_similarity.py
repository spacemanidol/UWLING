import nltk
import gensim
import sys
import re
from scipy.stats.stats import spearmanr
def remove_puncs(sentences):
    #remove punctuation and lowercase all words
    sentences_clean = []
    for sentence in sentences:
        clean = []
        for word in sentence:
            if not re.search('^\W+$', word):
                clean.append(word.lower())
        sentences_clean.append(clean)
    return sentences_clean
def read_judgments(filename):
    tuples = []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(',')
            tuples.append((l[0],l[1],float(l[2])))
    return tuples               
def main(window_size, judgement_filename, output_filename):
    sims,human = [],[]
    judgements = read_judgments(judgement_filename)
    sentences = remove_puncs(nltk.corpus.brown.sents())
    model = gensim.models.Word2Vec(sentences, min_count=0, workers=1, window=window_size, size=100, seed=1)
    with open(output_filename, 'w') as w:
        for word1, word2, judgement in judgements:
            sim = model.wv.similarity(word1, word2)
            sims.append(sim)
            human.append(judgement)
            w.write("{},{}:{}\n".format(word1,word2,sim))
        w.write("Correlation: {}\n".format(spearmanr(human, sims)[0]))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: hw7_cbow_similarity.sh <window> <judgment_filenname> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])