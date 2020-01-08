import sys
import os
def format_output(results, word):
    '''
    format the output into desired format of word/morph_tag
    args:results(str): results from carmel run, word(str):original word
    returns: to_output(str): formated output string
    '''
    to_output = ''
    end_part = 0
    i = 0
    j = 0 
    while i < len(results) - 1:
        if results[i] == '*e*': #if there was no trans state output just the letter
            to_output += word[j]
            i += 1
            j += 1
        else: #Transition state has a morph tag so output it and spacing
            to_output += '/'
            to_output += results[i]
            to_output += ' '
            i += 1
    return to_output.strip()

def main(fsm_filename, word_list_filename, output_filename):
    with open(word_list_filename, 'r') as f:
        with open(output_filename, 'w') as w:
            for l in f:
                formated_word = ''
                for letter in l:
                    formated_word = formated_word + ' ' + letter + ' ' #Split words into letters with space
                result = os.popen("echo '{}'| carmel -kO 1 -sli {}".format(formated_word,fsm_filename)).read().strip().split()
                if result == ['0']:
                    w.write("{} => *NONE*\n".format(l.strip()))
                else:
                    to_output = format_output(result,l)
                    w.write("{} => {}\n".format(l.strip(), to_output))
        
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: morph_acceptor2.py <fsm> <word_list> <output_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
