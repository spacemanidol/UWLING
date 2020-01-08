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


def multiple_final(fsa, end_state):
    '''
    Check if FSA has multiple roads to final state
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), end_state(str) an end state
    returns:(bool): a boolean representing if there are multiple finals
    '''
    count = 0
    for state in fsa:
        for rule in fsa[state]:
            if rule[1] == end_state:
                count += 1
        if count > 1:
            return True
    return False

def get_possible_transitions(states):
    '''
    Read in states and find out all possible transitions
    args:states(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string)
    returns:possible_transitions(dict) a dict of possible transitions
    '''
    possible_transitions = {}
    for state in states:
        for local in states[state]:
            possible_transitions[local[2]] = 1
    return possible_transitions

def remove_dupe(a_list):
    '''
    Remove Duplicate Values from a list
    args:a_list(list) a list of values
    returns:(list) of unique values without duplicates
    '''
    new_list = []
    for v in a_list:
        if v not in new_list:
            new_list.append(v)
    return new_list

#Recomended functions as per the instructions for hw3
def e_closure_s(fsa, s):
    '''
    provide the list of state accesible from a specific state via *e* transition
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), s(str), a state in the fsa
    returns:(list) of possible moves to be made
    '''
    moves = []
    for state in fsa[s]:
        if state[2] == '*e*':
            moves += [state[1]]
            moves += e_closure_s(fsa,state[1])
    return moves

def e_closure_S(fsa, S):
    '''
    provide the list of state accesible from a set of States e via *e* transition
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), S(list) a set of states
    returns:(list) of possible moves to be made
    '''
    moves = []
    for s in S:
        moves += [s]
        moves += e_closure_s(fsa,s)
    return remove_dupe(moves)
def move_nfa_S(fsa, S, a):
    '''
    provide the list of state accesible from a set of States e via transition
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), S(list) a set of states
    returns:(list) of possible moves to be made
    '''
    moves = []
    for s in S:
        moves += move_nfa_s(fsa,s, a)
    return remove_dupe(moves)

def move_nfa_s(fsa, s, a):
    '''
    provide the list of state accesible from a specific state via a transition
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), s(str), a state in the fsa
    returns:(list) of possible moves to be made
    '''
    moves = []
    if a == '' or s == '':
        return moves
    for state in fsa[s]:
        if state[2] == a:
            moves += [state[1]]
    return moves

def name_state(S):
    '''
    format state S into format mentioned in hw3 instructions
    args:S(list)a list of states
    returns:(str) a string in desire format
    '''
    output = ''
    for v in S:
        output += v
        output += '-'
    return output[:-1]

def remove_e(fsa):
    '''
    remove empty states, atifact I couldnt chase down in my code
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string)
    returns:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string)
    '''
    new_fsa = {}
    for state in fsa:
        new_fsa[state] = []
        for rule in fsa[state]:
            if rule[2] != '*e*':
                new_fsa[state].append(rule)
    return new_fsa

def convert_dfa_to_nfa(fsa, end_state, start_state):
    '''
    Conver dfa to NFA using algorith mentioned in class
    args:fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), end_state(str):end state of fsa, start_state(str):start of the fsa
    returns:dfa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), end_state(str):end state
    '''
    fsa[end_state] = []
    possible_transitions = get_possible_transitions(fsa)
    dfa = {start_state:[]} #add e-closure(s0) to sdfa as start_state
    S0 = remove_dupe(e_closure_S(fsa, [start_state]))
    S0.sort()
    dfa_visited = {name_state(S0):0} #Set the only state in SDFA to unmarked
    while 0 in dfa_visited.values(): # while sdfa contains unmarked state
        to_add = {}
        for v in dfa_visited:
            if dfa_visited[v] == 0:
                T = v.split('-')
                dfa_visited[v] = 1
                for a in possible_transitions:
                    S = remove_dupe(e_closure_S(fsa,move_nfa_S(fsa,T,a)))
                    S.sort()
                    S = name_state(S)
                    if S != '':
                        if S not in dfa_visited:
                            to_add[S] = 0
                        if v not in dfa:
                            dfa[v] = []
                        dfa[v].append((v, S, a ))
        for v in to_add:
            dfa_visited[v] = 0
    tmp = dfa
    dfa = remove_e(dfa)
    if multiple_final(dfa, end_state):
        dfa['FinalState'] = [(end_state, 'FinalState', '*e*')]
        end_state = 'FinalState'
    return dfa, end_state


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
                curr_char = rhs[1].replace(')','').replace(')','')#remove trailing )
                state = (curr_start, curr_end,curr_char)
                if curr_start not in states:
                    states[curr_start] = []
                states[curr_start].append(state)
    return states , str(end_state), str(start_state)

def print_dfa(states, end_state):
    '''
    Print DFA in desired format
    args: fsa(dict): a dict of lists(where keys are the state where a transition starts) of tuples where (Start State,End State, word/string), start state(str), end state(str)
    returns:None
    '''
    print('{}'.format(end_state))
    for state in states:
        for rule in states[state]:
            print('({} ({} {}))'.format(rule[0], rule[1], rule[2]))

if __name__ == "__main__":
    fsa_file = sys.argv[1].strip()
    fsa, end_state, start_state = load_fsa_file(fsa_file)
    if is_NFA(fsa):
        fsa, end_state = convert_dfa_to_nfa(fsa, end_state, start_state)
    print_dfa(fsa,  end_state)
