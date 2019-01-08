import sys
import os
import nltk
def remove_empty(a_list):
    b_list = []
    for item in a_list:
        if len(item) > 0:
            b_list.append(item)
    return b_list
def getPronouns(tree):
	pronouns = []
	for st in tree.subtrees():
		if st.label() in ['PRP', 'PossPro'] and len(st.leaves()) == 1:
			pronouns.append(st)
	return pronouns
def main(grammar_filename, test_sentence_filename, output_filename):
    grammar = nltk.data.load(grammar_filename)
    parser = nltk.parse.EarleyChartParser(grammar)
    sentences = remove_empty(nltk.data.load(test_sentence_filename).strip('\n').split('\n'))
    with open(output_filename, 'w') as w:
        i = 0
        while i < len(sentences)-1:
            tree1 = nltk.tree.ParentedTree.convert(list(parser.parse(nltk.word_tokenize(sentences[i])))[0])
            tree2 = nltk.tree.ParentedTree.convert(list(parser.parse(nltk.word_tokenize(sentences[i+1])))[0])
            prns = getPronouns(tree2)
            for prn in prns:
                w.write("{}\t{} {}\n".format(prn[0], tree1.pformat(margin=500), tree2.pformat(margin=500)))
            w.write('\n')
            i += 2
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:hw9_coref.py <lsinput_grammar_filename> <test_sentence_filename> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])