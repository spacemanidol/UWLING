import nltk
import numpy as np
import sys
import re
import math
from operator import itemgetter
from scipy.stats.stats import spearmanr
from scipy.spatial.distance import cosine
def remove_puncs(sentences):
    sentences_clean, words = [], set()
    for sentence in sentences:
        clean = []
        for word in sentence:
            if not re.search('^\W+$', word):
                clean.append(word.lower())
                words.add(word.lower())
        sentences_clean.append(clean)
    return sentences_clean, words  
def read_judgments(filename):
    tuples = []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(',')
            tuples.append((l[0],l[1],float(l[2])))
    return tuples                           
def print_results(output, output_filename):
    with open(output_filename,'w') as w:
        w.write(output)
def build_features(word, sentences, words, window):
    f, in_window = {}, set()
    for w in words:
        f[w] = 0
    for sentence in sentences:
        sentence = np.array(sentence).astype(str)
        sentence_l = len(sentence)
        for i in np.where(sentence == word)[0]:
            if i - window >= 0:
                index = int(i-window)
                f[sentence[index]] += 1
                in_window.add(sentence[index])
            if i + window < sentence_l:
                index = int(i+window)
                f[sentence[index]] += 1
                in_window.add(sentence[index])
    return f, in_window
def get_multiplier(words,sentences):
    f = {}
    for w in words:
        f[w] = 0
    for sentence in sentences:
        for word in sentence:
            f[word] += 1
    return sum(f.values()),f
def produce_output(f1,f2,word1,word2):
    output = ''
    out1 = word1
    out2 = word2
    m1 = sorted(f1.items(), key=itemgetter(0), reverse=False)
    m2 = sorted(f2.items(), key=itemgetter(0), reverse=False)
    cos_sim = 1 - cosine(list(list(map(list, zip(*m1)))[1]), list(list(map(list, zip(*m2)))[1]))
    m1 = sorted(f1.items(), key=itemgetter(1), reverse=True)
    m2 = sorted(f2.items(), key=itemgetter(1), reverse=True)
    for i in range(0, 10):
        out1 = out1 + ' ' + m1[i][0] + ':' + str(m1[i][1])
        out2 = out2 + ' ' + m2[i][0] + ':' + str(m2[i][1])
    output += out1
    output += '\n'
    output += out2
    output += '\n'
    output += word1 + ',' + word2 + ':' + str(cos_sim) + '\n'
    return output, cos_sim
def pmi(window, pairs, sentences, words):
    output = ''
    golden = []
    sims = []
    multiplier,count = get_multiplier(words,sentences)
    for word1, word2, sim in pairs:
        out1 = word1
        out2 = word2
        f1,w1 =  build_features(word1, sentences, words, window)
        f2,w2 =  build_features(word2, sentences, words, window)
        for word in w1:
            f1[word] = max(math.log2(f1[word] * multiplier / (count[word1] * count[word])), 0)
        for word in w2:
            f2[word] = max(math.log2(f2[word] * multiplier / (count[word2] * count[word])), 0)
        tmp, cos_sim = produce_output(f1,f2,word1,word2)
        sims.append(float(cos_sim))
        golden.append(float(sim))
        output += tmp
    output += 'Correlation:'+str(spearmanr(sims, golden)[0])
    return output
def freq(window, pairs, sentences, words):
    output = ''
    golden = []
    sims = []
    for word1, word2, sim in pairs:
        out1 = word1
        out2 = word2
        f1,w1 =  build_features(word1, sentences, words, window)
        f2,w2 =  build_features(word2, sentences, words, window)
        tmp, cos_sim = produce_output(f1,f2,word1,word2)
        sims.append(float(cos_sim))
        golden.append(float(sim))
        output += tmp
    output += 'Correlation:'+str(spearmanr(sims, golden)[0])
    return output
def main(window_size, weighting, judgement_filename, output_filename):
    judgements = read_judgments(judgement_filename)
    sentences, words = remove_puncs(nltk.corpus.brown.sents())
    if weighting == 'FREQ':
        print_results(freq(window_size,judgements, sentences, words), output_filename)
    elif weighting == 'PMI':
        print_results(pmi(window_size,judgements, sentences, words), output_filename)
    else:
        print('Please choose PMI or FREQ as weighting')
        exit(-1)
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: hw7_dist_similarity.sh <window> <weighting> <judgment_filenname> <output_filename>")
        exit(-1)
    else:
        main(float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])