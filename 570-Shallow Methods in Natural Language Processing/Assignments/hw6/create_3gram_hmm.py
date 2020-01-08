import os
import re
import sys
import math
def generate_header(unigrams, bigrams, words, pos, emissions, trans):
    return "state_num={}\nsys_num={}\ninit_line_num=1\ntrans_line_nun={}\nemiss_line_num={}\n\n\init\nBOS\t1.0\t0.0\n\n".format(len(pos), len(words), len(trans), len(emissions))
def sort_list(a_list):
    a_list.sort(key=lambda x:(x[1],x[0]))
    return a_list
def count(a_dict, key):
    if key in a_dict:
        return a_dict[key]
    else:
        return 0
def make_bis(a_dict):
    data = []
    for item in a_dict:
        for item2 in a_dict:
            data.append(item + '_' + item2)
    return data
def make_tris(a_dict):
    data = []
    for item in a_dict:
        for item2 in a_dict:
            for item3 in a_dict:
                data.append(item + '_' + item2 + '_' + item3)
    return data
def convert_ngram(ngram):
    pos = {}
    for item in ngram:
        if item[1] in pos:
            pos[item[1]] += ngram[item]
        else:
            pos[item[1]] = ngram[item]
    return pos
def load_unk(filename):
    data = {}
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split()
            data[l[0]] = float(l[1])
    return data
def load_training_data():
    sentences = []
    for line in sys.stdin:
        line = "<s>/BOS " + line.strip() + " <*s*>/EOS"
        line = re.sub(" +", " ", line)
        line = line.replace('\\/', '*\\*').split(' ')
        sentences.append(line)
    return sentences
def load_grams(sentences):
    unigrams, bigrams, trigrams, words = {}, {}, {} , {}
    for sentence in sentences:
        sent_len = len(sentence)
        for i in range(0, len(sentence)-2):
            w1 = (sentence[i].split('/')[0].replace('*\\*', '\\/'), sentence[i].split('/')[1])
            w2 = (sentence[i+1].split('/')[0].replace('*\\*', '\\/'), sentence[i+1].split('/')[1])
            w3 = (sentence[i+2].split('/')[0].replace('*\\*', '\\/'), sentence[i+2].split('/')[1])
            unigram = w1
            bigram = (w1[0] + ' ' + w2[0], w1[1] + ' ' + w2[1])
            trigram = (w1[0] + ' ' + w2[0] + ' '+ w3[0], w1[1] + ' ' + w2[1] + ' '+ w3[1])
            if unigram not in unigrams:
                unigrams[unigram] = 0
            if bigram not in bigrams:
                bigrams[bigram] = 0
            if trigram not in trigrams:
                trigrams[trigram] = 0
            if w1[0] not in words:
                words[w1[0]] = 0
            unigrams[unigram] += 1
            bigrams[bigram] += 1
            trigrams[trigram] += 1
        #funny, i tried to avoid having separate loops and it made not a clean
        w1 = (sentence[sent_len-2].split('/')[0].replace('*\\*', '\\/'), sentence[sent_len-2].split('/')[1])
        w2 = (sentence[sent_len-1].split('/')[0].replace('*\\*', '\\/'), sentence[sent_len-1].split('/')[1])
        bigram = (w1[0] + ' ' + w2[0], w1[1] + ' ' + w2[1])
        if w1 not in unigrams:
            unigrams[w1] = 0
        if w2 not in unigrams:
            unigrams[w2] = 0
        if bigram not in bigrams:
            bigrams[bigram] = 0
        unigrams[w1] += 1
        unigrams[w2] += 1
        bigrams[bigram] += 1
        if w1[0] not in words:
            words[w1[0]] = 0
        if w2[0] not in words:
            words[w2[0]] = 0
    words['<unk>'] = 0
    return unigrams, bigrams, trigrams, words

def get_emissions(unigrams, unknown):
    pos = list(convert_ngram(unigrams))
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
        smooth = 1
        if key in unknown:
            smooth = (1-unknown[key])
        for value in values:
            prob = smooth * (values[value]/total)
            for p in pos:
                i = p + '_' + key
                emissions[(value, i)] = prob
        for item in unknown:
            for p in pos:
                i = p + '_' + item
                emissions[('<unk>', i)] = unknown[item]
    return emissions

def get_trans(unigrams, bigrams, trigrams, l1, l2, l3):
    
    bigrams = convert_ngram(bigrams)
    unigrams = convert_ngram(unigrams)
    trigrams = convert_ngram(trigrams)
    possible_trigrams = make_tris(unigrams)
    s_unigram = sum(unigrams.values())
    t = len(unigrams)-2
    transitions = {}
    for trigram in possible_trigrams:
        split = trigram.split('_')
        pre_bigram = split[0] + ' ' + split[1]
        post_bigram = split[1] + ' ' + split[2]
        p1 = count(unigrams, split[2]) / s_unigram
        if split[1] == "EOS":
            if split[2] == "EOS":
                p2 = 1
                p3 = 1
            else:
                p2 = 0
                p3 = 0
        else: 
            p2 = count(bigrams, post_bigram) / count(unigrams, split[1])
            if split[2] == "BOS":  # current pos is BOS, p3 = 0
                p3 = 0
            elif count(bigrams, pre_bigram) == 0:  # previous bigram is not in training file
                p3 = 1/(t+1)
            else:
                p3 = count(trigrams, trigram) / count(bigrams, pre_bigram)
        p = l1 * p1 + l2 * p2 + l3 * p3
        transitions[trigram] = p
    return transitions
def sort_tran(trans):
    new_trans = {}
    for item in trans:
        word = item.replace('<*s*>', '</s>').split('_')
        w1 = word[0] + '_' + word[1]
        w2 = word[1] + '_' + word[2] 
        new_trans[(w2,w1)] = trans[item]
    return new_trans
def main(output_hmm_filename, l1, l2, l3, unknown_prob_filename):
    unk = load_unk(unknown_prob_filename)
    unigrams, bigrams, trigrams, words= load_grams(load_training_data())
    states = make_bis(convert_ngram(unigrams))
    emissions = get_emissions(unigrams, unk)
    trans = get_trans(unigrams, bigrams, trigrams, float(l1), float(l2), float(l3))
    with open(output_hmm_filename,'w') as w:
        w.write(generate_header(unigrams, bigrams, words, states, emissions, trans))
        w.write('\\transition\n')
        trans = sort_tran(trans)
        sort_trans = sort_list(list(trans.keys()))
        sort_emissions = sort_list(list(emissions.keys()))
        for item in sort_trans:
            prob =  float("%.10f" % float(trans[item]))
            lp = "%.10f" % math.log10(prob)
            w.write("{}\t{}\t{}\t{}\n".format(item[1],item[0],prob,lp))
        w.write('\n\\emission\n')
        for item in sort_emissions:
            word = item[0].replace('<*s*>', '</s>')
            prob =  float("%.10f" % float(emissions[item]))
            lp = "%.10f" % math.log10(prob)
            w.write("{}\t{}\t{}\t{}\n".format(item[1],word, prob,lp))
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:create_3gram_hmm.py <output_hmm> <l1> <l2> <l3> <unk_prob_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
