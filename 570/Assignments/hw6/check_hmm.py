import sys
def remove_empty(a_list):
    b_list = []
    for item in a_list:
        if len(item) > 0:
            b_list.append(item)
    return b_list
def read_init(items):
    data = {}
    for item in items:
        seq = remove_empty(item.split('\t'))
        if len(seq) == 1:
            seq = remove_empty(item.split(' '))
        if len(seq) > 1:
            data[(seq[0],seq[1])] = 0
    return data
def read_items(items):
    data = {}
    for item in items:
        seq = remove_empty(item.split('\t'))
        if len(seq) == 1:
            seq = remove_empty(item.split(' '))
        if len(seq) > 2:
            data[(seq[0],seq[1])] = float(seq[2])
    return data
def load_header(header):
    state_num = int(header[0].split('=')[1])
    sys_num = int(header[1].split('=')[1])
    init_line_num = int(header[2].split('=')[1])
    trans_line_num = int(header[3].split('=')[1])
    emiss_line_num = int(header[4].split('=')[1])
    return state_num, sys_num, init_line_num, trans_line_num, emiss_line_num
def generate_symbols(trans,emiss):
    states, symbols = [],[]
    for item in trans:
        if item[0] not in states:
            states.append(item[0])
        if item[1] not in states:
            states.append(item[1])
    for item in emiss:
        if item[0] not in states:
            states.append(item[0])
        if item[1] not in symbols:
            symbols.append(item[1])
    return states, symbols

def check(lines):
    lines = lines.split('\\init')
    state_num, sym_num, init_line_num, trans_line_num, emiss_line_num = load_header(remove_empty(lines[0].split('\n')))
    lines = lines[1].split('\\transition')
    init = read_init(remove_empty(lines[0].split('\n')))
    lines = lines[1].split('\\emission')
    trans = read_items(remove_empty(lines[0].split('\n')))
    emiss = read_items(remove_empty(lines[1].split('\n')))
    states, symbols = generate_symbols(trans,emiss)
    if state_num != len(states):
        print('warning: different numbers of state_num: claimed={}, read={}'.format(state_num,len(states)))
    else:
        print('state_num={}'.format(state_num))
    if sym_num != len(symbols):
        print('warning: different numbers of state_num: claimed={}, read={}'.format(sym_num,len(symbols)))
    else:
        print('sym_num={}'.format(sym_num))
    if init_line_num != len(init):
        print('warning: different numbers of init_line_num: claimed={}, read={}'.format(init_line_num,len(init)))
    else:
        print('init_line_num={}'.format(init_line_num))
    if trans_line_num != len(trans):
        print('warning: different numbers of trans_line_num: claimed={}, read={}'.format(trans_line_num,len(trans)))
    else:
        print('trans_line_num={}'.format(trans_line_num))
    if emiss_line_num != len(emiss):
        print('warning: different numbers of trans_line_num: claimed={}, read={}'.format(emiss_line_num,len(emiss)))
    else:
        print('emiss_line_num={}'.format(emiss_line_num))
    sum_init = 0
    for item in init:
        sum_init += float(item[1])
    if abs(sum_init - 1) > 0.0000000001:
        print('warning: the init_prob_sum is {}'.format(sum_init))
    for state in states:
        sum_t,sum_e = 0,0
        for item in trans:
            if item[0] == state:
                sum_t += trans[item]
        for item in emiss:
            if item[0] == state:
                sum_e += emiss[item]
        if abs(sum_t - 1) > 0.0000000001:
            print('warning: the trans_prob_sum for state {} is {}'.format(state, sum_t))
        if abs(sum_e - 1) > 0.0000000001:
            print('warning: the emiss_prob_sum for state {} is {}'.format(state, sum_e))

def main(input_hmm_filename):
    lines = ''
    with open(input_hmm_filename,'r') as f:
        for l in f:
            lines += l
    check(lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:check_hmm.py <input_hmm>")
        exit(-1)
    else:
        main(sys.argv[1])