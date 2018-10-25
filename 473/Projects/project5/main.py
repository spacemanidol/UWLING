import os
import string
import sys
import math
languages = ['dan','deu','dut','eng','fin','fra','gla','ita','nob','pol','por','spa','swe','swh','tgl']

def smoothing(corpus):
    '''
    Addative Smoothing
    args: corpus(dict): words to occourences based on langauge 
    returns: a modified corpus
    increase the count of each occourence to make zero count occourences 1 count. 
    '''
    for word in corpus:
        for lang in corpus[word]:
            corpus[word]['total'] += 1
            corpus[word][lang] += 1
    return corpus

def print_odds(odds, identifier, sentence, extra_credit):
    '''
    Print odds in correct format
    args: odds(dict) a dict of odds of a sentence coming from a specific language, identifier(str) unique identifier coming from intial file, sentence(str) a input string, extra_credit(Bool) 1 if appling extra credit
    returns:Nothing
    Take in the calculated information and print in correct format
    '''
    max_value = -1 * float('inf')
    max_lang = 'unk'
    print('{}\t{}'.format(identifier, sentence[:-1]))
    average_odds = 0
    for p in odds:
        average_odds += odds[p]
        if odds[p] > max_value:
            max_value = odds[p]
            max_lang = p
        print('{}\t{}'.format(p,odds[p]))
    difference = max_value - average_odds/15
    if extra_credit == 1 and difference < 25:
        print("result unk")
    else:
        print("result {}".format(max_lang))

def calculate_odds(corpus, sentence):
    '''
    Calculate odds of a specific langauge for an input sentence
    args: corpus(dict) a dict of words and count of occourences across words, sentence(str) a sentence that has been cleaned that we want to caclulate its probabilities across languages
    returns: probabilities(dict) a dict with langauge being the key and the value being the log prob of it occouring. Higher numbers = more likley
    take a sentence and use bayesean stat to calculate likleyhood of each langauge
    ''' 
    probabilities = {}
    for lang in languages:
        probability = float(0)
        for word in sentence:
            if word in corpus:
                probability +=  math.log10(float(corpus[word][lang])/float(corpus[word]['total']))
            else:
                probability += math.log10(0.06666666666666667
)
        probabilities[lang] = probability
    return probabilities

def load_corpus(corpus_directory):
    '''
    Read a corpus and normalize
    args: corpus_directory(str) a location where expected corpus files exist
    returns: a corpus(dict) structure with the smoothed occourences of words across langauges
    Function reads all the corpuses in a directory and then normalizes their occourences using additive smoothing
    '''
    corpus = {}
    target_files = os.listdir(corpus_directory)
    for target_file in target_files:
        file_path = os.path.join(corpus_directory, target_file)
        with open(file_path,'r') as f:
            lang = target_file[:3]
            for l in f:
                l = l.split('\t')
                target_word = l[0]
                target_value = int(l[1])
                if target_word not in corpus:
                    corpus[target_word] = {'dan':0,'deu':0,'dut':0,'eng':0,'fin':0,'fra':0,'gla':0,'ita':0,'nob':0,'pol':0,'por':0,'spa':0,'swe':0,'swh':0,'tgl':0}
                corpus[target_word][lang] = target_value
    for word in corpus:
        unique_total = 0
        for lang in languages:
            unique_total += corpus[word][lang]
        corpus[word]['total'] = unique_total
    return smoothing(corpus)

def main(corpus_locaiton, target_file, extra_credit):
    '''
    Read a corpus and caculate most probable langauge for given sentences
    args: corpus_location(str) a location of a directory of corpuses, target_file(str) a file with sentences we want to calculate most likley langauges
    Load a corpus, smooth it, use it to calculate most likley langauges for files
    '''
    corpus = load_corpus(corpus_location)
    with open(target_file,'r') as f:
        for l in f:
            l = l.split('\t')
            sentence = l[1].strip()
            sentence = sentence.translate(None, string.punctuation) 
            print_odds(calculate_odds(corpus,sentence.split(' ')), l[0], l[1], extra_credit)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: main.py <target dna strings> <location of dna corpus> <flag extra credit>")
        exit(-1)
    else:
        corpus_location = sys.argv[1]
        target_file = sys.argv[2]
        extra_credit = int(sys.argv[3])
        main(corpus_location, target_file, extra_credit)
