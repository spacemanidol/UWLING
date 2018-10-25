import os
import sys

class node:
    def __init__(self, char, is_done):
        self.char = char
        self.children = [None] * 4
        self.is_done = is_done    
    def add(self, to_add):
        """Add a child node based on its character
        Args:to_add(node) a new node we want to be a child of current node
        Returns:None
        Only gets added if matches one of the 4 DNA letters
        """
        if to_add.char == 'A':
            self.children[0] = to_add
        elif to_add.char == 'C':
            self.children[1] = to_add
        elif to_add.char == 'G':
            self.children[2] = to_add
        elif to_add.char == 'T':
            self.children[3] = to_add

class trie:
    def __init__(self):
        self.head = node("head",False)

    def get(self):
        return self.head

    def add(self, search_word):
        """Adds target sequence to trie
        Args:search_word(str) a word to be added to the trie
        Returns:None
        Starting at the trie head, we add loop over the word letter by letter adding children if they dont exist. When done set final state to is_done(meaning final character)
        """
        current = self.head
        for i in search_word:
            if i == 'A':
                if current.children[0] == None:
                    current.add(node(i,False))
                current = current.children[0]
            elif i == 'C':
                if current.children[1] == None:
                    current.add(node(i,False))
                current = current.children[1]
            elif i == 'G':
                if current.children[2] == None:
                    current.add(node(i,False))
                current = current.children[2]
            elif i == 'T':
                if current.children[3] == None:
                    current.add(node(i,False))
                current = current.children[3]
        current.is_done = True   

def get_files_in_dir(dir_path):
    """Finds all files in a directory and returns as a sorted list
    Args:dir_path(str) a folder where there are files
    Returns:alist(list) a list of all files in the directory sorted alphabetically by filename
    """
    alist = os.listdir(dir_path)
    alist.sort()
    return alist

def populate_trie_with_target(a_trie, target_sequences):
    """Read from a file with target sequences and load them into a trie structure
    Args:a_trie(trie) , target_sequences(str) a filename with target DNA sequences
    Returns:a_trie(trie) populated with all target strings.
    This function reads the file and then line by line loads them into the trie for future search
    """
    with open(target_sequences, 'r') as f:
        for line in f:
            a_trie.add(line.strip().upper())
    return a_trie

def find_matches(a_trie, dna_corpus):
    """Finds target DNA sequences in list of chromosomes
    Args:target_strings(str) a file location of target strings, dna_corpus(str) a folder location of chromosones
    Returns:None
    """
    files = get_files_in_dir(dna_corpus)
    extra_credit = {}
    for file in files:
        filepath = os.path.join(dna_corpus, file)
        print(filepath)
        with open(filepath, 'r') as f:
            input_text = f.read().upper() 
            input_text_len = len(input_text)
            i = 0
            while i < input_text_len:
                j = i
                current = a_trie.get()
                while j < input_text_len:
                    current_char = input_text[j]
                    if current_char == 'A' and current.children[0] != None:
                        current = current.children[0]
                    elif current_char == 'C' and current.children[1] != None:
                        current = current.children[1]
                    elif current_char == 'G' and current.children[2] != None:
                        current = current.children[2]
                    elif current_char == 'T' and current.children[3] != None:
                        current = current.children[3]
                    elif current.is_done == True:
                        target_string = input_text[i:j]
                        offset = str(format(i, '08X'))
                        print("\t"+ offset +"\t" + target_string)
                        if target_string not in extra_credit:
                            extra_credit[target_string] = []
                        extra_credit[target_string].append('\t'+offset+'\t'+filepath)
                        break
                    else:
                        break
                    j += 1
                i += 1
    with open('extra-credit','w') as w:
        for target_string in extra_credit:
            w.write(target_string+'\n')
            for key in extra_credit[target_string]:
                w.write(key+'\n')

def main(target_strings, dna_corpus):
    """Finds target DNA sequences in list of chromosomes
    Args:target_strings(str) a file location of target strings, dna_corpus(str) a folder location of chromosones
    Returns:None
    """
    a_trie = trie()
    a_trie = populate_trie_with_target(a_trie, target_strings)
    find_matches(a_trie, dna_corpus)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py <target dna strings> <location of dna corpus>")
        exit(-1)
    else:
        target_strings = sys.argv[1]
        dna_corpus = sys.argv[2]
        main(target_strings,dna_corpus)
