import sys
import os
def isnumber(string):
    return any(i.isdigit() for i in string)
def ishyphen(string):
    return any(i=='-' for i in string)
def isupper(string):
    return any(i.isupper() for i in string)
def sort_list(dict):
   return [v[0] for v in sorted(dict.items(), key=lambda kv: (-kv[1], kv[0].upper()))]
def add(a_list, target):
    if target not in a_list:
        a_list.append(target)
    return a_list  
def output_file(path, words, filename):
    words_list = sort_list(words)
    with open(os.path.join(path, filename),'w') as w:
        for word in words_list:
            w.write('{} {}\n'.format(word,words[word]))
def remove_under_threshold(features, threshold, path):
    kept = {}
    dropped = []
    for feature in features:
        if feature[0:4] == 'curW':
            kept[feature] = features[feature]
            continue
        if features[feature] < threshold:
            dropped.append(feature)
            continue
        else:
            kept[feature] = features[feature]
    output_file(path,kept,'kept_feats')
    return dropped
def process_line(sentence, index, features, rare_threshold, dropped):
    words, tags, features = create_features_sentences(sentence, features, rare_threshold)
    i = 0
    to_write = ''
    for feature in features:
        if words[i+2] == ',':
            words[i+2] = 'comma'
        if tags[i+2] == ',':
            tags[i+2] = 'comma'
        to_write += "{}-{}-{} {}".format(str(index), str(i), words[i+2], tags[i+2])
        for item in feature:
            if item in ['containNum', 'containUC', 'containHyp']:
                continue
            if item not in dropped:
                item = item.replace(',','comma')
                if item in ['containNum 1','containUC 1','containHyp 1']:
                    to_write += ' {}'.format(item)
                else:
                    to_write += ' {} 1'.format(item)
            else:
                continue
        to_write += '\n'
        i += 1
    return to_write        
def process_file(input_filename, features, rare_threshold, dropped, output_filename):
    with open(output_filename,'w') as w:
        with open(input_filename,'r') as f:
            j=1
            for l in f:
                w.write(process_line(l.strip().split(' '),j,features,rare_threshold,dropped))
                j += 1  
def create_features_sentences(sentence, words, rare_threshold):
    sent_words, sent_tags, features =  ['BOS','BOS'], ['BOS','BOS'], []
    for item in sentence:
        if '\/' in item:
            tmp = item.split('\/')
            word = tmp[0] + '\/' + tmp[1].split('/')[0]
            tag = tmp[1].split('/')[1]
        else:
            word, tag = item.split('/')
        sent_tags.append(tag)
        sent_words.append(word)
    sent_tags.append('EOS')
    sent_tags.append('EOS')
    sent_words.append('EOS')
    sent_words.append('EOS')
    for i in range(2,len(sent_words)-2):
        to_add,length = [],[1,2,3,4]
        to_add = add(to_add, 'prevW='+sent_words[i-1])
        to_add = add(to_add, 'prev2W='+sent_words[i-2])
        to_add = add(to_add, 'nextW='+sent_words[i+1])
        to_add = add(to_add, 'next2W='+sent_words[i+2])
        to_add = add(to_add, 'prevT='+sent_tags[i-1])
        to_add = add(to_add, 'prevTwoTags='+sent_tags[i-2]+'+'+sent_tags[i-1])
        if words[sent_words[i]] >= rare_threshold:
            to_add.insert(0, 'curW={}'.format(sent_words[i]))
        else:
            for j in length:
                if len(sent_words[i]) >= j:
                    if len(sent_words[i][0:j-1]) > 1:
                        to_add = add(to_add, 'pref={}'.format(sent_words[i][0:j-1]))
                    to_add = add(to_add, 'suf={}'.format(sent_words[i][-(j):]))
            if isnumber(sent_words[i]):
                to_add.append('containNum')
            if isupper(sent_words[i]):
                to_add.append('containUC')
            if ishyphen(sent_words[i]):
                to_add.append('containHyp')
        features.append(to_add)
    return sent_words, sent_tags, features
def create_features(filename, words, rare_threshold, path):
    features = {}
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            _,_, items = create_features_sentences(l,words,rare_threshold)
            for feature in items:
                for item in feature:
                    if item in ['containNum', 'containUC', 'containHyp']:
                        continue
                    if item not in features:
                        features[item] = 1
                    else:
                        features[item] += 1
    output_file(path,features,'init_feats')
    return features
def load_file(filename):
    words = {}
    with open(filename,'r') as f:
        for l in f:
            if len(l) == 0:
                continue
            else:
                l = l.strip().split(' ')
                for item in l:
                    if '\/' in item:
                        tmp = item.split('\/')
                        word = tmp[0] + '\/' + tmp[1].split('/')[0]
                    else:
                        word = item.split('/')[0]
                    if word not in words:
                        words[word] = 0
                    words[word] += 1
    return words
def main(train_filename, test_filename, rare_threshold, feature_threshold, output_directory):
    train_words= load_file(train_filename)
    output_file(output_directory, train_words, 'train_voc')
    test_words = load_file(test_filename)
    train_words['comma'] = train_words[',']
    test_words['comma'] = test_words[',']
    features = create_features(train_filename,train_words,rare_threshold, output_directory)
    dropped = remove_under_threshold(features, feature_threshold, output_directory)
    process_file(train_filename, train_words, rare_threshold, dropped, os.path.join(output_directory, "final_train.vectors.txt"))
    process_file(test_filename, test_words, rare_threshold, dropped, os.path.join(output_directory, "final_test.vectors.txt"))
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage:maxent_tagget.py <train filename> <test filename> <rare threshold> <feature threshold> <output_dir>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])