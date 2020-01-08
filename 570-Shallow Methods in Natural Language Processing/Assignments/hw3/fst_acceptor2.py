import sys
import os
def is_ambiguous(fst):
    '''
    Since we have not covered Viterbi algorithm, fst_acceptor2.sh will handle only
    non-ambiguous FST; that is, if you ignore the output symbols on the arcs, the
    resulting FSA is a DFA, not an NFA. 
    Main things NFA can have that a DFA cant:1. Epsilon,2.More than one transition for each input at each state
    args:fst(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string)
    returns:(bool): a boolean representing if its an NFA or not
    '''
    for state in fst:
        inputs_seen_so_far = {}
        for transition in fst[state]:
            if transition[2] == "*e*": ##Transition
                return True
            elif transition[2] in inputs_seen_so_far: #if therfe are multiple paths for the same input from a given state then it can't be a DFA
                return True
            inputs_seen_so_far[transition[2]] = 1
    return False

def load_fst_file(filename):
    '''
    Load an FST into my represenation
    args:filename(str) string representing file location of fsa to be loaded
    returns:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str)
    open the fsa file, read into our structure while we remove unwanted characters. Then Check if is_ambiguous, if it is, then we write error message and exit
    '''
    end_state = ''
    start_state = ''
    states = {}
    header = 0
    header_2 = 0
    with open(filename, 'r') as f:
        for l in f:
            if header == 0:
                header = 1
                end_state = l.strip()
            else:
                l = l.split("(") 
                if header_2 == 0:
                    header_2 = 1
                    start_state = str(l[1].strip())
                if len(l) < 3:
                    continue
                curr_start = l[1].strip()
                rhs = l[2][:-2].strip().replace(")","").split(" ")
                prob = 1
                if len(rhs) == 4:
                   prob = float(rhs[3])
                curr_end = rhs[0]
                curr_char = rhs[1]
                replacement_char = rhs[2]
                state = (curr_start, curr_end,curr_char, replacement_char, prob)
                state = (curr_start, curr_end, curr_char)
                if curr_start not in states:
                    states[curr_start] = []
                states[curr_start].append(state)
    if is_ambiguous(states):  
        sys.stderr.write("The input  FST is ambiguous\n")
        exit(-1)
    return states , str(end_state), str(start_state)
    
def accepts(fst, input, end_state, start_state):
    '''
    Check if a input is accepted by a FST
    args:fst(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string, replacement, probability), start state(str), end state(str), input(list  of str) a line of text we want to see if is accepted by fst
    returns:bool on if a string is accepted by dfa, output(str): the updated transformed string, probability(float) the probability of said string being transformed
    run input through DFA. If it reaches end of input and is in end state True, else false
    '''
    current_state = start_state
    output = ''
    probability = 1
    for value in input:
        possible_moves = fst[current_state]
        can_transition = False
        for move in possible_moves:
            if move[2] == value:
                can_transition = True
                current_state = move[1]
                if move[2] != '*e*': 
                    output += move[2]
                if len(move) == 4:
                    probability = probability * move[4]
        if can_transition == False:
            return False, '', 0
    if current_state == end_state:
        return True, output, probability
    return False, '', 0        

def run_fst_on_file(input_file, fst, end_state, start_state):
    '''
    Open file and then see for each line if the FST accepts or not
    args:fst(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str), input_file(str) location of a file we want to analyze
    returns:None
    Open a file, run each line through DFA and output results
    '''
    with open(input_file, 'r') as f:
        for l in f:
            l1 = l.strip().split(" ")
            a, output, prob = accepts(fst,l1,end_state, start_state)
            if a:
                print("{}=>{} {}".format(l.strip(), output, prob))
            else:
                print("{}=>*none* 0".format(l.strip()))

if __name__ == "__main__":
    fst_file = sys.argv[1]
    input_file = sys.argv[2]
    fst, end_state, start_state = load_fst_file(fst_file)
    run_fst_on_file(input_file,fst,end_state,start_state)
