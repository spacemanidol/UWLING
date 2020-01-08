import os
import sys
def sort_list(dict):
    return [v[0] for v in sorted(dict.items(), key=lambda kv: (-kv[1], kv[0].upper()))]
def load_sentences(training_data_filename):
    sentences = []
    with open(training_data_filename,'r') as f:
        for l in f:
            sentences.append('<s> ' + l.strip() + ' </s>')
    return sentences
def count_unigrams(sentences):
    unigrams = {}
    for sentence in sentences:
        sentence = sentence.split(' ')
        for word in sentence:
            if word not in unigrams:
                unigrams[word] = 0
            unigrams[word] += 1
    return unigrams
def count_bigrams(sentences):
    bigrams = {}
    for sentence in sentences:
        sentence = sentence.split(' ')
        for i in range(0,len(sentence)-1):
            word = sentence[i] + ' ' + sentence[i+1]
            if word not in bigrams:
                bigrams[word] = 0
            bigrams[word] += 1
    return bigrams
def count_trigrams(sentences):
    trigrams = {}
    for sentence in sentences:
        sentence = sentence.split(' ')
        for i in range(0,len(sentence)-2):
            word = sentence[i] + ' ' + sentence[i+1] + ' ' + sentence[i+2]
            if word not in trigrams:
                trigrams[word] = 0
            trigrams[word] += 1
    return trigrams
def print_ngrams(unigrams, bigrams, trigrams, ngram_count_filename):
    with open(ngram_count_filename, 'w') as w:
        for word in sort_list(unigrams):
            w.write("{}	{}\n".format(unigrams[word], word))
        for word in sort_list(bigrams):
            w.write("{}	{}\n".format(bigrams[word], word))
        for word in sort_list(trigrams):
            w.write("{}	{}\n".format(trigrams[word], word))
def main(training_data_filename, ngram_count_filename):
    sentences = load_sentences(training_data_filename)
    unigrams = count_unigrams(sentences)
    bigrams = count_bigrams(sentences)
    trigrams = count_trigrams(sentences)
    print_ngrams(unigrams, bigrams, trigrams, ngram_count_filename)    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:ngram_count.py <training_data> <ngram_count_file")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2])
