import nltk
import sys
class Node:
    '''
    Node class which serves as the base of the tree we build up
    '''
    def __init__(self, root, left_branch, right_branch, word, start, end, prob):
        self.root = root
        self.left_branch = left_branch
        self.right_branch = right_branch
        self.word = word
        self.start = start
        self.end = end
        self.prob = prob

def parse(trees, start_symbol):
    '''
    Given a list of trees, create the parse for each tree.
    args:trees(list) a list of trees(Nodes connecting to other nodes), start_symbol(str) a start symbol from the grammar
    returns:, output(str) formated output of parses
    Loop through each tree and pass on to parse_tree function. Keep track of how many parses are possible
    '''
    max = 0.0 #floats are fun
    max_node = None
    output = ''
    for node in trees:
        if node.prob > max:
            max = node.prob
            max_node = node
    if max_node != None:
        if max_node.root == start_symbol:
            output += str(parse_tree(max_node))
    return output

def parse_tree(node):
    '''
    Given a node in a tree build up a nltk representation for a tree
    args:node(Node) a node in a tree we wish to turn itno a nltk tree
    returns: tree(NLTK Tree) full parse for the sentenc
    Loop through each node, if there is a word, then its terminal and return, else recurse through left and right branch until they become terminal
    '''
    if  node.word != None:
        return nltk.tree.Tree(str(node.root),[str(node.word)])
    else:
        return nltk.tree.Tree(str(node.root), [parse_tree(node.left_branch), parse_tree(node.right_branch)])

def cky(grammar, input_sentence):
    '''
    Given a grammar and input string, use CKY algorithm to generate parse strings
    args:grammar(list) a list of productions in a grammar, input_sentece(str) a sentence we want to parse
    returns:(list) a list of nodes of the roots of acceptable parses
    Use CKY algorithm with a back pointer as described in class to generate information on every possible parse.
    '''
    n = len(input_sentence)
    table = [[[] for i in range(n+1)] for j in range(n+1)]
    bp = [[[] for i in range(n+1)] for j in range(n+1)]
    for j in range(1,n+1):
        for grammar_rule in grammar:
            lhs = grammar_rule._lhs
            if input_sentence[j-1] in grammar_rule._rhs:
                table[j-1][j].append(lhs)
                bp[j-1][j].append(Node(lhs, None, None, input_sentence[j-1]),j-1,j-1,float(grammar_rule.prob()))
        for i in reversed(range(0,j-1)):
            for k in range(i+1,j):
                for grammar_rule in grammar:
                    lhs = grammar_rule._lhs
                    if len(grammar_rule._rhs) == 2:
                        if grammar_rule._rhs[0] in table[i][k] and grammar_rule._rhs[1] in table[k][j]:
                            table[i][j].append(lhs)
                            for b in bp[i][k]:
                                for c in bp[k][j]:
                                    if b.root == grammar_rule._rhs[0] and c.root == grammar_rule._rhs[1]:
                                        bp[i][j].append(Node(grammar_rule._lhs, b, c, None, b.start, b.end,float(grammar_rule.prob()) b.prob * c.prob))   
    return bp[0][n]
def main(grammar_file, input_file, output_file):
    '''
    Open a grammar file and test input file and produce all possible parses for each given sentence
    Args: grammar_file(str): a filename for a cfg file, input_file(str): a filename of input file containing sentences to be parsed, output_file(str): a filename where results should be writen.
    Returns: None
    Open the file, read line, tokenize, use cky to create parse trees and then print said trees
    '''
    grammar = nltk.data.load(grammar_file)
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as w:
            counts = [] #save the amount of parse trees in a list
            for line in f:
                w.write(line)
                parses = parse(cky(grammar.productions(), nltk.word_tokenize(line)), grammar.start())
                w.write("{}\n".format(parses)) 

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: parser.py <grammar_file> <test_sentence_filename> <output_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])