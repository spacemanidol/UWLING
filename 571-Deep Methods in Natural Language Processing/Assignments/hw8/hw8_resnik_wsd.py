import nltk
import sys
from scipy.stats.stats import spearmanr
from nltk.corpus import *
from nltk.corpus.reader.wordnet import information_content
def read_wsd(filename):
    words = []
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split('\t')
            words.append((l[0], l[1].split(',')))
    return words
def read_judgments(filename):
    tuples = []
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(',')
            tuples.append((l[0],l[1],float(l[2])))
    return tuples  
def resnik(word1, word2, ic):
    word1 = wordnet.synsets(word1)
    word2 = wordnet.synsets(word2)
    sim = {}
    if word2 == []:
        return (('NOSENSE','NOSENSE'),0)
    for syn1 in word1:
        for syn2 in word2:
            common = syn1.common_hypernyms(syn2)
            if len(common) > 0:
                sim[(syn1,syn2)] = max(information_content(s,ic) for s in common)
            else:
                sim[(syn1,syn2)] = 0
    return sorted(sim.items(), key = lambda x:-x[1])[0]             
def main(wsd_filename, judgement_filename, output_filename):
    sims,human = [],[]
    ic = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    judgements = read_judgments(judgement_filename)
    wsds = read_wsd(wsd_filename)
    with open(output_filename, 'w') as w:
        for wsd in wsds:
            word = wsd[0]
            senses = {}
            output = ''
            for noun in wsd[1]:
                r = resnik(word, noun, ic)
                if str(r[0][0]) == 'NOSENSE':
                   output += "({}, {},0) ".format(word,noun)
                else:
                    sense = r[0][0].name()
                    sim = r[1]
                    output += "({}, {}, {}) ".format(word,noun, sim)
                    if sense not in senses:
                        senses[sense] = 0
                    senses[sense] += sim
            w.write("{}\n{}\n".format(output[:-1], sorted(senses.items(), key = lambda x:-x[1])[0][0]))
        for judgement in judgements:
            word1 = judgement[0]
            word2 = judgement[1]
            sim = resnik(word1, word2, ic)[1]
            w.write("{},{}:{}\n".format(word1, word2, sim))
            sims.append(sim)
            human.append(judgement[2])
        w.write("Correlation:{}\n".format(spearmanr(human, sims)[0]))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: hw8_resnik_wsd <wsd_filename> <judgment_filenname> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1],sys.argv[2],sys.argv[3])