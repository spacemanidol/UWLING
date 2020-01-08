import os
import re
import sys
import math
def generate_header(unigrams, bigrams, words, pos, emissions, trans):
    return "state_num={}\nsys_num={}\ninit_line_num=1\ntrans_line_nun={}\nemiss_line_num={}\n\n\init\nBOS\t1.0\t0.0\n\n".format(len(pos), len(words), len(trans), len(emissions))
def sort_list(a_list):
    a_list.sort(key=lambda x:(x[0],x[1]))
    return a_list
def load_training_data():
    sentences = []
    for line in sys.stdin:
        line = "<s>/BOS " + line.strip() + " <*s*>/EOS"
        line = re.sub(" +", " ", line)
        line = line.replace('\\/', '*\\*').split(' ')
        sentences.append(line)
    return sentences

def convert_ngram(ngram):
    pos = {}
    for item in ngram:
        if item[1] in pos:
            pos[item[1]] += ngram[item]
        else:
            pos[item[1]] = ngram[item]
    return pos

def get_trans(unigrams,bigrams):
    bigrams = convert_ngram(bigrams)
    unigrams = convert_ngram(unigrams)
    transitions = {}
    for key in bigrams:
        w1 = key.split(' ')[0]
        w2 = key.split(' ')[1]
        prob = bigrams[key]/ unigrams[w1]
        transitions[(w1,w2)] = prob
    return transitions

def get_emissions(unigrams):
    emissions, state_symbols = {}, {}
    for ngram in unigrams:
        if ngram[1] not in state_symbols:
            state_symbols[ngram[1]] = {}
            state_symbols[ngram[1]][ngram[0]] = 0
        elif ngram[1] in state_symbols and ngram[0] not in state_symbols[ngram[1]]:
            state_symbols[ngram[1]][ngram[0]] = 0
        state_symbols[ngram[1]][ngram[0]] += unigrams[ngram]
    for key in state_symbols:
        values = state_symbols[key]
        total = sum(values.values())
        for value in values:
            emissions[(value, key)] = values[value]/total
    return emissions

def load_grams(sentences):
    unigrams, bigrams, words, pos = {}, {}, {} , {}
    for sentence in sentences:
        sent_len = len(sentence)
        for i in range(0, len(sentence)-1):
            w1 = (sentence[i].split('/')[0].replace('*\\*', '\\/'), sentence[i].split('/')[1])
            w2 = (sentence[i+1].split('/')[0].replace('*\\*', '\\/'), sentence[i+1].split('/')[1])
            unigram = w1
            bigram = (w1[0] + ' ' + w2[0], w1[1] + ' ' + w2[1])
            if unigram not in unigrams:
                unigrams[unigram] = 0
            if bigram not in bigrams:
                bigrams[bigram] = 0
            if w1[0] not in words:
                words[w1[0]] = 0
            if w1[1] not in pos:
                pos[w1[1]] = 0
            unigrams[unigram] += 1
            bigrams[bigram] += 1
        #funny, i tried to avoid having separate loops and it made not a clean
        w1 = (sentence[sent_len-1].split('/')[0].replace('*\\*', '\\/'), sentence[sent_len-1].split('/')[1])
        if w1 not in unigrams:
            unigrams[w1] = 0
        unigrams[w1] += 1
        if w1[0] not in words:
            words[w1[0]] = 0
        if w1[1] not in pos:
            pos[w1[1]] = 0
    return unigrams, bigrams, words, pos
def main(output_hmm_filename):
    unigrams, bigrams, words, pos = load_grams(load_training_data())
    emissions = get_emissions(unigrams)
    trans = get_trans(unigrams,bigrams)
    with open(output_hmm_filename,'w') as w:
        w.write(generate_header(unigrams, bigrams, words, pos, emissions, trans))
        w.write('\\transition\n')
        sort_trans = sort_list(list(trans.keys()))
        sort_emissions = sort_list(list(emissions.keys()))
        for item in sort_trans:
            word = item[0].replace('<*s*>', '</s>')
            prob =  float("%.10f" % float(trans[item]))
            lp = "%.10f" % math.log10(prob)
            w.write("{}\t{}\t{}\t{}\n".format(word,item[1],prob,lp))
        w.write('\n\\emission\n')
        for item in sort_emissions:
            word = item[0].replace('<*s*>', '</s>')
            prob =  float("%.10f" % float(emissions[item]))
            lp = "%.10f" % math.log10(prob)
            w.write("{}\t{}\t{}\t{}\n".format(item[1],word, prob,lp))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:create_2gram_hmm.py <output_hmm>")
        exit(-1)
    else:
        main(sys.argv[1])
