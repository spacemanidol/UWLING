import sys
import math
def remove_empty(a_list):
    b_list = []
    for item in a_list:
        if len(item) > 0:
            b_list.append(item)
    return b_list
def get_pos(emiss):
    pos = {}
    for item in emiss:
        if item[1] not in pos:
            pos[item[1]] = [item[0]]
        else:
            pos[item[1]] = pos[item[1]] + [item[0]]
    return pos
def read_items(lines):
    data, symbols = {}, {}
    for line in lines:
        seq = remove_empty(line.strip(' ').split('\t'))
        if len(seq) == 1:
            seq = remove_empty(line.split(' '))
        if len(seq) == 2:
            if float(seq[1]) > 1:
                print("warning: the prob is not in [0,1] range:{}".format(line), file=sys.stderr)
            else:
                data[(seq[0])] = float(seq[1])
        if len(seq) > 2:
            if float(seq[2]) > 1:
                print("warning: the prob is not in [0,1] range:{}".format(line), file=sys.stderr)
            else:
                data[(seq[0], seq[1])] = float(seq[2])
                symbols[seq[1]] = 1
    return data, symbols
def read_hmm(input_hmm_filename):
    lines = ''
    with open(input_hmm_filename,'r') as f:
        for l in f:
            lines += l
    lines = lines.split('\\init')
    lines = lines[1].split('\\transition')
    pi, _ = read_items(remove_empty(lines[0].split('\n')))
    lines = lines[1].split('\\emission')
    transitions, _ = read_items(remove_empty(lines[0].split('\n')))
    emissions, symbols = read_items(remove_empty(lines[1].split('\n')))
    pos = get_pos(emissions)
    return pi, transitions, emissions, symbols, pos
def read_test(test_filename, symbols):
    tests = []
    with open(test_filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            s = line.split(' ')
            for i in range(0, len(s)):
                if s[i] not in symbols:
                    s[i] = "<unk>"
            tests.append([s, line])
    return tests
def viterbi(pi, transitions, emissions, symbols, pos, line):
    states = {} 
    for init in pi:
        states[init] = ([init], math.log10(pi[init]))
    for word in line:
        new_states = {}
        for current in states:
            for next in pos[word]:
                if (current, next) in transitions and (next, word) in emissions:
                    lp = math.log10(emissions[(next, word)]) + math.log10(transitions[(current, next)]) + states[current][1]
                    if next in new_states:
                        if lp > new_states[next][1]:
                            new_states[next] = (states[current][0] + [next], lp)
                    else:
                        new_states[next] = (states[current][0] + [next], lp)
        states = new_states
    if len(states) > 0:
        lgs = {}
        for state in states:
            lgs[states[state][1]] = state
        return states[lgs[max(lgs.keys())]]
    else:
        return ()
def main(input_hmm_filename, test_filename, output_filename):
    pi, transitions, emissions, symbols, pos = read_hmm(input_hmm_filename)
    test = read_test(test_filename, symbols)
    with open(output_filename,'w') as w:
        for item in test:
            t = viterbi(pi, transitions, emissions, symbols, pos, item[0])
            if len(t) == 0:
                w.write('{} => *NONE*\n'.format(item[1]))
            else:
                output = ''
                for state in t[0]:
                    output = output +  ' ' + state
                w.write('{} =>{} {}\n'.format(item[1], output, t[1]))
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: viterbi.py <input_hmm_filename> <test_filename> <output_filename>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])