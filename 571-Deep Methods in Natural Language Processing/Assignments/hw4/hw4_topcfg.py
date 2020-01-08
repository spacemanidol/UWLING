from collections import defaultdict, Counter
import sys
import nltk

from collections import defaultdict, Counter
from nltk import tree
from nltk import PCFG

def indentify_productions_probabilities(sentences):
    rules = []
    mappings = defaultdict(Counter)
    totals = Counter()
    for sentence in sentences:
        parse = nltk.tree.ParentedTree.fromstring(sentence)
        productions = parse.productions()
        for production in productions:
            rules.append(production)
            mappings[production._lhs][production._rhs] += 1
            totals[str(production._lhs)] += 1
    return set(rules), mappings, totals
def induce_PCFG(rules, mappings, totals, output_PCFG_filename):
    with open(output_PCFG_filename,'w') as w:
        for production in rules:
            left_hand_side = production._lhs
            right_hand_side = production._rhs
            probability = mappings[left_hand_side][right_hand_side]/totals[str(left_hand_side)]
            w.write("{} [{}]\n".format(str(production),str(probability)))
def read_parsed_sentences(treebank_filename):
    sentences = []
    with open(treebank_filename,'r') as f:
        for l in f:
            sentences.append(l)
    return sentences
            
def main(treebank_filename, output_PCFG_filename):
    parsed_sentences = read_parsed_sentences(treebank_filename)
    rules, mappings, totals  = indentify_productions_probabilities(parsed_sentences)
    induce_PCFG(rules, mappings, totals, output_PCFG_filename)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: hw4_topcfg.py <treebank_filename> <output_PCFG_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2])
