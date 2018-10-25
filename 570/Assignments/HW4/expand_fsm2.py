import sys
import os
def load_lexicon(lexicon_filename):
    lexicon = {}
    with open(lexicon_filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            while(len(l) > 2):
                l.remove('')
            if l[0] != '':
                if l[1] not in lexicon:
                    lexicon[l[1]] = []
                lexicon[l[1]].append(l[0])
    return lexicon

def load_morph(morph_rules_filename):
    rules = []
    start_state = ''
    end_state = ''
    header = 0
    with open(morph_rules_filename, 'r') as f:
        for l in f:
            if header == 0:
                end_state = l.strip()
                header += 1
            else:
                l = l.strip().replace(')', '').split('(')
                if l != ['']:
                    start = l[1].strip()
                    l = l[2].split(' ')
                    if header == 1:
                        start_state = start
                        header += 1
                    transition = l[1]
                    end = l[0]
                    rules.append((start,end,transition))
    return rules, start_state, end_state

def split_letters_in_word(rules):
    new_rules = []
    for rule in rules:
        if rule[2] == '*e*':
            new_rules.append(rule)
        else:
            start_state = rule[0]
            new_start = start_state+ '_' + rule[2] + '_' + rule[2][0]
            new_rules.append((start_state, new_start, '*e*', '*e*'))
            for i in range(0, len(rule[2])-1):
                new_start = start_state+ '_' + rule[2] + '_' + rule[2][i]
                new_trans = start_state + '_' + rule[2] + '_' + rule[2][i+1]
                new_rules.append((new_start,new_trans, rule[2][i], '*e*'))
            new_rules.append((start_state+'_' + rule[2] + '_'+rule[2][-1:],rule[1],rule[2][-1:], rule[3]))
    return new_rules

def print_fsm(filename, rules, end):
    with open(filename,'w') as w:
        w.write('{}\n'.format(end))
        for rule in rules:
            w.write('({} ({} {} {}))\n'.format(rule[0],rule[1],rule[2], rule[3]))
    
def main(lexicon_filename, morphology_rules_filename, output_fsm_filename):
    lexicon = load_lexicon(lexicon_filename)
    morph, start, end = load_morph(morphology_rules_filename)
    new_rules = []
    for rule in morph:
        if rule[2] == '*e*':
            new_rules.append((rule[0],rule[1],rule[2], '*e*'))
        else:
            associated = lexicon[rule[2]]
            for word in associated:
                new_rules.append((rule[0],rule[1],word, rule[2]))
    new_rules = split_letters_in_word(new_rules)
    print_fsm(output_fsm_filename,new_rules,end)
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: expand_fsm2.py <lexicon> <morphology_rules> <output_fsm>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])