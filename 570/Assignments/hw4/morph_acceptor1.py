import sys
import os

def main(fsm_filename, word_list_filename, output_filename):
    with open(word_list_filename, 'r') as f:
        with open(output_filename, 'w') as w:
            for l in f:
                formated_word = ''
                for letter in l.strip():
                    formated_word = formated_word + ' ' + letter + ' ' #Split word into leters
                result = os.popen("echo '{}'|carmel -sli {}".format(formated_word,fsm_filename)).read().strip()
                if result != '':
                    w.write("{} => yes\n".format(l.strip()))
                else:
                    w.write("{} => no\n".format(l.strip()))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: morph_acceptor1.py <fsm> <word_list> <output_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])