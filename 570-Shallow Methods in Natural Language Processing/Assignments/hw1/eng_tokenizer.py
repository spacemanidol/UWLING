"""
Read input, break tokens into whitespace and output frequency of tokens
Creation Date: 10/01/2018
Lasf Modified: 10/04/2018
Authors: Daniel Campos <dacampos@uw.edu>
"""
import os
import sys
import re


EMAIL = re.compile(r"\w+@\w") #assumtions that anything with an @ sign is an email because I dont know other rules around domains
URL = re.compile(r"(?:(?:https?|http|ftp|smtp|git)://)?\w+(?:\.\w+)+") #any type of website
PHONE = re.compile(r"(\(\d{3}\)) (\d{3}\-\d{4})") # USA phone number style patern clean
PHONE_REV = re.compile(r"(\(\d{3}\))\-(\d{3}\-\d{4})") #USA phone number style to convert back into desired phone format
PATH = re.compile(r"[A-Z]:/") #Path all assuming that it must contain at least one upper case letter followed by :/ such as C:/
TILDE = re.compile(r"(~/\w)")#tilde PATH
CONTRACTIONS = re.compile(r"(^\w+)(n't|'(?:d|re|s|m|all))") # any type of english contraction such as don't and 'all
PUNCTUATION = re.compile(r"""``|''|[?\/|~@!":-]""") 
PERIOD = re.compile(r"(\.)(?!\d)") # period not before a digit
NEGATIVE = re.compile(r"^(?:-\d)")# Negative before a digit
DOLLAR = re.compile(r"(\$)") #Dolla Dolla Bill yall
COMMA = re.compile(r"(,)(?!\d)") # comma not preceding a digit
FRACTION = re.compile(r"\d/\d") # Fraction
TILDE = re.compile(r"(~/\w)")#tilde PATH
DASH = re.compile(r"--")
ELIPSES = re.compile(r"\w...")
INITIAL =  re.compile(r"[A-Z][a-z]?\.(?:[A-Z][a-z]?\.)*") #initials and abbreviation
def punctuation_recurse(a_string, pattern):
    '''given a string and a regex pattern splits on any match
    args:a_string(str) a string, patter(regex compiled search pattern) a punctuation pattern.
    returns string split by punct
    '''
    output = []
    match = pattern.search(a_string)
    if match:
        punct = match.group()
        punct_index = a_string.index(punct) 
        output.extend([a_string[:punct_index], punct])
        output.extend(punctuation_recurse(a_string[punct_index+len(punct):], pattern))
    else:
        output.append(a_string)
    return [x for x in output if x]
    
def main(abbreviation_filename):
    '''Takes input from stdin, tokenizes
    Args:abbreviation_filename(str) a file with a list of abbreviations
    Returns:None
    Take lines to STDIN input, split on whitespace a
    '''
    abbreviations = []
    with open(abbreviation_filename,'r') as f:
        for line in f:
            abbreviations.append(re.compile(line.strip())) #Turn each abbreviation into a searchable regex
    abbreviations = abbreviations[:-1] #remove empty abbreviation last newline per format in files seen so far
    for line in sys.stdin:
        line = PHONE.sub(r"\1-\2", line) #ensure phones dont split
        output = []
        tokens = line.split()
        for token in tokens:
            is_url = URL.search(token)
            if is_url:
                output.append(token)
                continue
            is_email = EMAIL.search(token)
            if is_email:
                output.append(token)
                continue
            is_path = PATH.search(token)
            if is_path:
                output.append(token)
                continue
            is_tilde = TILDE.search(token)
            if is_tilde:
                output.append(token)
                continue
            is_negative = NEGATIVE.search(token)
            if is_negative:
                output.append(token)
                continue
            is_fraction = FRACTION.search(token)
            if is_fraction:
                output.append(token)
                continue
            is_dash = DASH.search(token)
            if is_dash:
                output.append(token)
                continue
            is_elipses = ELIPSES.search(token)
            if is_dash:
                output.append(token)
                continue
            is_initial = INITIAL.search(token)
            if is_initial:
                output.append(token)
                continue
            is_abbreviation = 0
            for abbreviation in abbreviations:
                abbreviation_result = abbreviation.search(token)
                if abbreviation_result:
                    is_abbreviation = 1
                    break
            if is_abbreviation == 1:
                output.append(token)
                continue
            token = CONTRACTIONS.sub(r"\1 \2", token) 
            token = ' '.join(punctuation_recurse(token,PUNCTUATION))
            token = COMMA.sub(r" \1", token)
            token = PERIOD.sub(r" \1", token)
            output.append(token)
        line = ' '.join(output)
        line = PHONE_REV.sub(r"\1 \2", line)
        line = line.replace('$','$ ')
        line = line.replace('\'s',' \'s')
        line = line.replace('.,','. ,')
        line = line.replace('%','% ')
        line = line.replace('  ',' ')#remove double space
        line = line.replace('  ',' ')#remove double space
        print(" " + line)         
            
if __name__ == '__main__':
    main(sys.argv[1])
