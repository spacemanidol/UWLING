import nltk
import sys
from nltk.parse import FeatureEarleyChartParser

def load_fcfg(grammar_filename):
    '''
    load a grammar file
    Args: grammar_filename(str): a filename for a fcfg
    Returns: nltk grammar
    '''
    return nltk.parse.FeatureEarleyChartParser(nltk.data.load(grammar_filename,  format='fcfg'))

def load_test_sentences(input_sentence_filename):
    '''
    load a test sentences
    Args: input_sentence_filename(str): a filename of a target input sentences file
    Returns: sentences(list): a list of sentences to parse
    '''
    sentences = []
    with open(input_sentence_filename,'r') as f:
        for l in f:
            sentences.append(l)
    return sentences

def parse(parser, sentence):
    '''
    Try and parse a sentence given a grammar
    Args: parser(EarlyChartPasrset): a parser initialized using created cfg, sentence(Str) a sentence to be parsed
    Returns: (str) of the results. Empty if doesnt parse, with parses if it does
    '''
    tokens = nltk.word_tokenize(sentence)
    for item in parser.parse(tokens):
        return item.pformat(margin=sys.maxsize)
    return ''

def main(grammar_filename, input_sentence_filename, output_filename):
    '''
    Open a grammar file and test input file and produce all possible parses for each given sentence
    Args: grammar_file(str): a filename for a cfg file, input_file(str): a filename of input file containing sentences to be parsed, output_file(str): a filename where results should be writen.
    Returns: None
    Open the file, read line, tokenize, use cky to create parse trees and then print said trees
    '''
    parser = load_fcfg(grammar_filename)
    sentences = load_test_sentences(input_sentence_filename)
    with open(output_filename, 'w') as w:
        for sentence in sentences:
            w.write("{}\n".format(parse(parser, sentence).replace('(NP[] )',''))) #Removing this empty NP thing I would do
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: hw5_parser.py <input_grammar_file> <input_sentence_filename> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])