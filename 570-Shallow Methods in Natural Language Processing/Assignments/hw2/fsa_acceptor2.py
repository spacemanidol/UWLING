import sys
import os
def is_NFA(fsa):
    '''
    Main things NFA can have that a DFA cant:1. Epsilon,2.More than one transition for each input at each state
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string)
    returns:is_nfa(bool): a boolean representing if its an NFA or not
    '''
    for state in fsa:
        inputs_seen_so_far = {}
        for transition in fsa[state]:
            if transition[2] == "*e*": ##Transition
                return True
            elif transition[2] in inputs_seen_so_far: #if therfe are multiple paths for the same iput from a given state then it can't be a DFA
                return True
            inputs_seen_so_far[transition[2]] = 1
    return False

def load_fsa_file(filename):
    '''
    Load an FSA into my represenation
    args:filename(str) string representing file location of fsa to be loaded
    returns:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str)
    open the fsa file, read into our structure while we remove unwanted characters. Then Check if is_NFA, if it is, then we write error message and exit
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
                curr_start = l[1].strip()
                rhs = l[2][:-2].strip().split(" ")
                curr_end = rhs[0]
                curr_char = rhs[1][:-1]#remove trailing )
                state = (curr_start, curr_end,curr_char)
                if curr_start not in states:
                    states[curr_start] = []
                states[curr_start].append(state)
    states[end_state] = []
    if is_NFA(states):
        sys.stderr.write("The input {} is an NFA\n".format(filename))
        exit(-1)
    return states , str(end_state), str(start_state)
    
def accepts(fsa, input, end_state, start_state):
    '''
    Check if a input is accepted by a DFA
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str), input(list  of str) a line of text we want to see if is accepted by dfa
    returns:bool on if a string is accepted by dfa
    run input through DFA. If it reaches end of input and is in end state True, else false
    '''
    current_state = start_state
    for value in input:
        possible_moves = fsa[current_state]
        can_transition = False
        for move in possible_moves:
            if move[2] == value:
                can_transition = True
                current_state = move[1]
                break
        if can_transition == False:
            return False
    if current_state == end_state:
        return True
    return False        

def run_fsa_on_file(input_file, fsa, end_state, start_state):
    '''
    Open file and then see for each line if the DFA accepts or not
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str), input_file(str) location of a file we want to analyze
    returns:None
    Open a file, run each line through DFA and output results
    '''
    with open(input_file, 'r') as f:
        for l in f:
            l1 = l.strip().split(" ")
            if accepts(fsa,l1,end_state, start_state):
                print("{}=>yes".format(l.strip()))
            else:
                print("{}=>no".format(l.strip()))

if __name__ == "__main__":
    fsa_file = sys.argv[1]
    input_file = sys.argv[2]
    fsa, end_state, start_state = load_fsa_file(fsa_file)
    run_fsa_on_file(input_file,fsa,end_state,start_state)
