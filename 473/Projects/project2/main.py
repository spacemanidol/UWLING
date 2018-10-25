"""
This module computes unigram counts in a corpus
To execute please execute ./run.sh or python3 main.py
Creation Date: 08/07//2018
Lasf Modified: 08/14/2018
Authors: Daniel Campos <dacampos@uw.edu>
"""
import os
import sys
import re

def read_and_prep_file(filename):
    """Read contents of a file,remove html tags
    Args: filename(str): a filename with full path to be loaded
    Returns: text(str): a string containing all words
    We read in all lines in a file, join into one long string, remove all html, turn any character that isnt A-Z and ' into a ' ', then remove trailing and leading 's and convert to lower
    """
    with open(filename, 'r') as f:
        clean_text = ''.join(f.readlines())
    clean_text = re.sub('<.*?>', '', clean_text) #remove html lines
    clean_text = re.sub('[^A-Za-z\']', ' ', clean_text) #replace illegal characters with space
    clean_text = re.sub(' \'*',' ', clean_text) #remove leading '
    clean_text = re.sub('\'* ', ' ', clean_text).lower() # remove trailing ' and convert to lower
    return clean_text

def print_official_score(values):
    """Print Output in desired format
    Args:values(dict): a dict of keys(type) and count.
    Returns:None
    Print unique values sorted by value high to low
    """
    for v in sorted(values, key= values.get, reverse=True):
        print('{}\t{}'.format(v,values[v]))

def calculate_unigrams(directory_path):
    """Find Files, Read them, clean and count word occourances
    Args:directory_path(str): a path where prd files are located
    Returns:None
    Read all files, clean the text and turn into a list before looping over it to get unique counts of each word
    """
    target_files = os.listdir(directory_path)
    formated_text = ''
    unigrams = {}
    for target_file in target_files:
        formated_text += read_and_prep_file(os.path.join(directory_path, target_file))
    all_clean_words = re.findall(r"[\w']+",formated_text) #find all unique words. I found this was ~ 1 minute faster than spliting
    for word in all_clean_words:
        if word not in unigrams: #avoid key error
            unigrams[word] = 0
        unigrams[word] += 1
    print_official_score(unigrams)        

if __name__ == '__main__':
    calculate_unigrams('/corpora/LDC/LDC02T31/nyt/2000')
