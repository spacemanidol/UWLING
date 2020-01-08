import nltk
import sys
def main(grammar_file, input_file, output_file):
    '''Read the sentences in a file, generate parse trees and count average amount of trees
    Args: grammar_file(str): a filename for a cfg file, input_file(str): a filename of
     input file containing sentences to be parsed, output_file(str): a filename where results should be writen.
    Take in a grammar file and use it with NLTK tooling to create a parser. Next open the input file and for 
    each sentence produce a parse tree. At each point add the ammount of parse trees that can be created to a
     list. Once all sentences are read calcualte the average amount of parse trees using the list
    '''
    grammar = nltk.data.load(grammar_file)
    parser = nltk.parse.EarleyChartParser(grammar)
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as w:
            counts = [] #save the amount of parse trees in a list
            for line in f:
                w.write(line)
                parses = 0
                tokens = nltk.word_tokenize(line)
                for item in parser.parse(tokens):
                    parses += 1
                    w.write(str(item)+"\n")
                w.write("Number of parses: {}\n\n".format(parses))
                counts.append(parses)
            w.write("Average parses per sentence: {}\n".format(round(sum(counts)/len(counts),3)))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: main.py <grammar file> <input sentence file> <output file name>")
        exit(-1)
    else:
        grammar_file = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        main(grammar_file, input_file, output_file)
