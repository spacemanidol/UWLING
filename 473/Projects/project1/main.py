"""
This module computes the occourances of various constituent types found in a folder of prd files.

To execute please execute ./run.sh or python3 main.py

Creation Date: 07/30/2018
Lasf Modified: 08/02/2018
Authors: Daniel Campos <dacampos@microsoft.com>

"""
import os
import sys
import nltk_tgrep as tgrep
from nltk import SExprTokenizer
from nltk.tree import ParentedTree

def get_files_in_dir(directory_path):
    """Get all files in a path
    Args: directory_path(str) : path  where target files are located
ted
    Returns: list_of_files (list): a list that contains all the file names in the directory
    """
    return os.listdir(directory_path)

def read_and_prep_file(filename):
    """Read contents of a file, tokenize contents and turn into a tree
    Args: filename(str): a filename with full path to be loaded
    Returns: ptree (parented tree nltk object): a tree object native to NLTK that automatically maintains parent pointer in every node.     
    First off we initiallize SExprTokenizer a tool in nltk used to find parenthesized expressions 
    """
    tokenizer = SExprTokenizer()
    with open(filename, 'r') as f:
        tmp_strings = tokenizer.tokenize(''.join(map(str.strip,f.readlines()))) #read all the lines(f.readlines() produces a list), strip all bad characters(spaces, newlines, etc) and join into one large senteze and then use the SE tokenizer
        return [ParentedTree.fromstring(tmp) for tmp in tmp_strings] # for each string in file terun a tree 

def count_occurrences(tree,pattern,constituent_filter):
    """Take a tree, a desired search pattern and a filter and return a count
    Args:tree (ptree): a ParentedTree of a sentence, pattern (str): a pattern to search for, constituent(lambda filter): a filter condition based on desired properties
    Returns: count_of_constituents
    We take a tree and search for all matches in it using tgrep(tree grep) then we remove all matches that dont match out fiter. For S, VP, NP we set the filter to None, for IVP and DVP we set the appropirate conditions 
    """
    matches = tgrep.tgrep_nodes(tree, pattern) #find all items in tree that match our searc pattern
    constituents = list(filter(constituent_filter, matches)) #remove whatever doesnt match our filter
    return len(constituents)

def print_official_score(values):
    """Print Output in desired format
    Args:values(dict): a dict of keys(type) and count.
    Returns:None
    """
    for v in values:
        print('{}\t{}'.format(v,values[v]))

def calculate_constituents(directory_path):
    """Find Files, Read them, and calculate counts of various constituents across a directory
    Args:directory_path(str): a path where prd files are located
    Returns:None
    Simple process to get all constituents: 1. Find all file names in a directory, 2. Open them and turn them into ptrees, 3. use tgrep and filet using lambdas to get desired values, 4. output scores in desired format
    """
    constituent_counts = {'Sentence':0, 'Verb Phrase':0, 'Noun Phrase':0,'Ditransitive Verb Phrase':0, 'Intransitive Verb Phrase':0}
    if os.path.isdir(directory_path):
        target_files = get_files_in_dir(directory_path)
        for target_file in target_files:
            trees = read_and_prep_file(directory_path+'/'+target_file)
            for tree in trees:
                constituent_counts['Sentence'] += count_occurrences(tree,'S', None)
                constituent_counts['Noun Phrase'] += count_occurrences(tree,'NP', None)
                constituent_counts['Verb Phrase'] += count_occurrences(tree,'VP', None)
                constituent_counts['Ditransitive Verb Phrase'] += count_occurrences(tree,"VP < (NP $ NP)", lambda x: len(x) == 3)
                constituent_counts['Intransitive Verb Phrase'] += count_occurrences(tree,"VP", lambda x: len(list(x.subtrees())) == 1)
        print_official_score(constituent_counts)
    else:
        print('Error: Invalid directory Path \"{}\". please confirm correct directory exits'.format(directory_path))
        exit(-1)
if __name__ == '__main__':
    calculate_constituents('/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14')
