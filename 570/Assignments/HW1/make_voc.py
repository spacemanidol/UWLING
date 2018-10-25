"""
Read input, break tokens into whitespace and output frequency of tokens
Creation Date: 10/01/2018
Lasf Modified: 10/04/2018
Authors: Daniel Campos <dacampos@uw.edu>
"""
import sys

def print_unigram_count(values):
    """Print Output in desired format
    Args:values(dict): a dict of keys(type) and count.
    Returns:None
    Print unique values sorted by value high to low
    """
    for v in sorted(values, key= values.get, reverse=True):
        print('{}\t{}'.format(v,values[v]))
        
def main():
    '''Takes input from stdin, splits and then performs a count
    Args:None
    Returns:None
    Take lines to STDIN input, split on whitespace and then use a dictionary to keep counts
    '''
    unigrams = {}
    for line in sys.stdin:
        all_words = line.strip().replace('\t',' ').split(' ')
        for word in all_words:
            if word not in unigrams:
                unigrams[word] = 0
            unigrams[word] += 1
    unigrams.pop('') #remove empty count
    print_unigram_count(unigrams)
if __name__ == '__main__':
    main()
