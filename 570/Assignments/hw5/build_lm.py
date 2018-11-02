import os
import math
import sys
def sort_list(dict):
   return [v[0] for v in sorted(dict.items(), key=lambda kv: (-kv[1], kv[0].upper()))]
def load_data(ngram_count_file):
    ngrams = ({},{},{})
    with open(ngram_count_file,'r') as f:
        for l in f:
            l = l.split('\t')
            t = len(l[1].split(' ')) - 1
            ngrams[t][l[1].strip()] = int(l[0])
    return (ngrams[0], ngrams[1], ngrams[2])
def get_data(ngrams):
    types = len(ngrams)
    tokens = 0
    for ngram in ngrams:
        tokens += ngrams[ngram]
    return types, tokens
    
def analyze_data(ngrams):
    to_print = ''
    for i in range(0,len(ngrams)):
        types, tokens = get_data(ngrams[i])
        to_print += 'ngram {}: type={} token={}\n'.format(i+1,types,tokens) 
    return to_print

def calc_ngram(word, ngrams, tokens):
    count = ngrams[word]
    prob = "%.10f" % float(count/tokens)
    logprob = "%.10f" % math.log10(count/tokens)
    if prob == 1 or prob == '1.0000000000':
        prob = '1'
        logprob = '0'
    return '{} {} {} {}\n'.format(count, prob, logprob, word)

def main(ngram_count_filename, lm_filename):
    ngrams = load_data(ngram_count_filename)
    analyze_data(ngrams)
    prop = '\ '
    with open(lm_filename,'w') as w:
        w.write('\data\ \n')
        w.write(analyze_data(ngrams))
        w.write('\n{}1-grams:\n'.format(prop[:-1]))
        types, tokens = get_data(ngrams[0])
        for word in sort_list(ngrams[0]):
            w.write(calc_ngram(word,ngrams[0],tokens))
        w.write('\n{}2-grams:\n'.format(prop[:-1]))
        for word in sort_list(ngrams[1]):
            w.write(calc_ngram(word,ngrams[1],ngrams[0][word.split(' ')[0]]))
        w.write('\n{}3-grams:\n'.format(prop[:-1]))
        for word in sort_list(ngrams[2]):
            split_word = word.split(' ')
            word1 = split_word[0] + ' ' + split_word[1]
            w.write(calc_ngram(word,ngrams[2],ngrams[1][word1]))
        w.write('\end\ \n')        
 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:build_lm.py <ngram_count_file> <lm_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2])
