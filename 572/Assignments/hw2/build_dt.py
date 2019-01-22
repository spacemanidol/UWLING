import sys
import numpy as np
import math
import os

class Node:
    def __init__(self, path, data, features, depth, label, result):
        self.path = path
        self.data = data
        self.features = features
        self.depth = depth
        self.label = label
        self.p_child = None
        self.n_child = None
        self.feature = ''
        self.result = result

def explore_node(node, w, labels):
    if node.p_child != None:
        explore_node(node.p_child,labels)
        explore_node(node.n_child,labels)
    else:
        print(node.data)
        out = "{} {}".format(node.path.strip('&'),str(node.data.shape[1]))
        for label in node.result:
            out += " {} {}".format(label, str(node.result[l]))
        w.write('{}\n'.format(out))

def write_dt(root, filename):
    with open(filename, 'w') as w:
        explore_node(root, w, set(root.data[0]))

def entropy(items):
    s = sum(items)
    probabilities = []
    for item in items:
        probabilities.append(item/s)
    s = 0
    for item in probabilities:
        if item > 0:
            s += item*math.log2(item)
    return -s

def get_info_gain(original_data, positive_data, negative_data, labels):
    if positive_data.shape[1] == 0 or negative_data.shape == 0:
        return 0
    probs = [[],[],[]]
    data = [original_data, positive_data, negative_data]
    for label in labels:
        for i in range(0,3):
            probs[i].append((data[i][0] == l).sum())
    return entropy(probs[0]) - (sum(probs[1]) * entropy(probs[1])/sum(probs[0])) - sum(probs[2]) * (entropy(probs[2])/sum(probs[0]))    

def read_data(filename):
    labels, features= [],[]
    with open(filename, 'r') as f:
        for l in f:
            l = l.strip().split(' ')
            labels.append(l[0])
            features.append([i.split(":")[0] for i in l[1:]])
    features = set()
    for feature in features:
        features += set(feature)
    return np.array([labels, features]), features #second value should be a set containing all potential features

def get_leaf(node, features):
    if node.p_child != None:
        if node.feature in features:
            return find_leaf(node.p_child, features)
        else:
            return find_leaf(node.n_child, features)
    else:
        return node
def split_samples(data, item):
    labels, features = data[0], data[1]
    positive = [i in item for item in features]
    negative = [i not in item for item in features]
    positive_labels = labels[positive]
    negative_label = labels[negative]
    positive_featues = features[positive]
    negative_features = features[negative]
    return np.array([positive_labels, positive_featues]), np.array([negative_label, negative_features])

def write_output(root, training_data, test_data, filename):
    result,truth = [[],[]], [[],[]]
    with open(filename, 'w') as w:
        for item in to [(0,'training', training_data), (1,'test', test_data)]:
            w.write("%%%%% {} data:\n".format(item[1]))
            for i in range(len(item[2])):
                out = 'array:{}'.format(i)
                leaf = get_leaf(root,item[2][0][i])
                label = item[2][1][i]
                result[item[0]].append(leaf.label)
                truth[item[0]].append(label)
                for feature in leaf.result:
                    out += ' {} {}'.format(result,leaf.result[feature])
                w.write("{}\n".format(out))
    return result, truth

def print_confusion_matrix(result, truth):
    lookup = {1:'train', 2:'test'}
    for i in range(2):
        print("Confusion matrix for the {} data:\nrow is the truth, column is the system output\n".format(lookup[i]))
        labels = list(set(truth[i]))
        d = len(labels)
        result_length = len(result[i])
        m = np.zeros([d,d])
        label2idx, idx2label = {}, {}
        index, count = 0, 0
        for label in labels:
            label2idx[label] = index
            idx2label[index] = label
            index += 1
        for j in range(result_length):
            m[result[i][j]][truth[i][j]] += 1
            if result[i][j] == truth[i][j]:
                count += 1
        out = ''
        for j in range(d):
            out += ' {}'.format(idx2label[i])
        out += '\n'
        for j in range(d):
            out += label2idx[j]
            for k in range(d):
                out += ' {}'.format(str(int(m[j][k])))
            out += '\n'
        print("            {}\n {} accuracy={}\n".format(out, lookup[i], count/result_length))

def build_tree(training_data, features, max_depth, min_gain):
    tree, a_path, split_last_iteration  = [], set() , True
    root = Node('', training_data, [], 0, '', {})
    tree.append(root)
    labels = set(training_data[0])
    while split_last_iteration:  #keep going until no more splits happen
        split_last_iteration = False
        new_tree = []
        for node in tree:
            if node.path in a_path:
                new_tree.append(node)
            else:
                best = ''
                max_info_gain = 0
                if node.depth < max_depth:
                    data = node.data
                    for feature in features.difference(set(node.features)):
                        positive, negative = split_samples(data, feature)
                        info_gain = get_info_gain(data, positive, negative, labels)
                        if info_gain > max_info_gain:
                            best = feature
                            max_info_gain = info_gain
                    if max_info_gain > min_gain:
                        positive, negative =  split_samples(data, best)
                        samples, to_insert = [positive, negative],[]
                        for i in range(2):
                            occourences = Counter(samples[i][0])
                            results = {}
                            for label in labels:
                                if label in occourences:
                                    p = samples[i].get(label)/samples[i].shape[1]
                                else:
                                    p = 0
                                result[label] = p
                            if i == 0:
                                path = node.path + best + '&'
                            else:
                                path = node.path + '!' + best + '&'
                            f = node.features
                            f. append(best)
                            new_node = Node(path, samples[i], f, node.depth+1, occourences.most_common(1)[0][0], result)
                            new_tree.append(new_node)
                            node.feature = best
                            to_insert[i] = new_node
                        node.p_child(to_insert[0])
                        node.n_child(to_insert[0])
                        new_tree.append(node)
                        a_path.add(node.path)
                        split_last_iteration = True
                    else:
                        new_tree.append(node)
                        a_path.add(node.path)
        if split_last_iteration == 1:
            tree = new_tree
    return root

def main():
    training_data, features = read_data(sys.argv[1])
    test_data, _ = read_data(sys.argv[2])
    root = build_tree(training_data, features, int(sys.argv[3]), float(sys.argv[4]))
    write_dt(root, sys.argv[5])
    result, truth = write_output(root, training_data, test_data, sys.argv[6])
    write_matrix(result, truth)

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage:build_dt.py <training_data> <test_data> <max_depth> <min_gain> <model_file> <sys.output>")
        exit(-1)
    else:
        main()