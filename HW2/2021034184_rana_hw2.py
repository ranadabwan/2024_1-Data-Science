import math
import sys


def InfoGain(values):
    """
    Calculates the entropy of a given list
    """
    sum = 0
    result = 0.0

    for v in values:
        sum = sum + v

    for x in values:
        if x == 0 or sum == 0:
            continue

        p = x / sum
        result = result - p * math.log2(p)

    return result

def calculate_domain_counts(database, categories, index):
    frequency = [0 for _ in categories[index]]
    domain_index = {k: i for i, k in enumerate(categories[index])}

    for data_tuple in database:
        frequency[domain_index[data_tuple[index]]] += 1

    return frequency

class TreeNode:
    """
    A node in decision tree 
    """
    def __init__(self, feat):
        self.feat = feat
        self.next = []
        self.result = 'invalid'

    def append(self, newNode):
        self.next.append(newNode)

    def setFeat(self, feat):
        self.feat = feat

    def setResult(self, result):
        self.result = result

    def getFeat(self):
        return self.feat

    def getNext(self, index):
        return self.next[index]

    def getResult(self):
        return self.result

def set_criteria(database, attr, attr_check_list, kind):
    """
    Recursively building the decision tree
    """
    ret = TreeNode(-1)

    # InfoGain(D)
    ret_cnt = calculate_domain_counts(database, kind, -1)
    all_info = InfoGain(ret_cnt)

    if all_info == 0:
        ret.setResult(database[0][-1])
        return ret

    gain_list = []
    tmp=len(attr) - 1
    for a in range(tmp):

        if attr_check_list[a] == True:
            gain_list.append(-123456789)
            continue

        info_a = 0.0
        for k in kind[a]:

            idx = 0
            ret_domain = {}                                
            cond_cnt = [0 for i in range(len(kind[-1]))]   

            for tuple in database:
                if tuple[a] != k:
                    continue

                if tuple[-1] not in ret_domain:
                    ret_domain[tuple[-1]] = idx
                    cond_cnt[idx] = cond_cnt[idx] + 1
                    idx = idx + 1
                else:
                    cond_cnt[ret_domain[tuple[-1]]] = cond_cnt[ret_domain[tuple[-1]]] + 1

            info_a_k = InfoGain(cond_cnt)                             # 
            info_a = info_a + sum(cond_cnt) / len(database) * info_a_k  

        gain_a = all_info - info_a  
        gain_list.append(gain_a)

    
    max_gain_idx = gain_list.index(max(gain_list))
    ret.setFeat(max_gain_idx)

    dc = calculate_domain_counts(database, kind, -1)            
    max_dc_idx = dc.index(max(dc))          
    max_label = list(kind[-1])[max_dc_idx]  

    for k, i in zip(kind[max_gain_idx], range(len(kind[max_gain_idx]))):

        newDB = [tuple for tuple in database if tuple[max_gain_idx] == k]

        if len(newDB) == 0:
            newNode = TreeNode(-1)
            newNode.setResult(max_label)
            ret.append(newNode)
            continue

        new_attr_check_list = attr_check_list.copy()
        new_attr_check_list[max_gain_idx] = True

        subNode = set_criteria(newDB, attr, new_attr_check_list, kind)
        ret.append(subNode)

    return ret

def find_class_rec(node, kind, tuple):
    """
    Recursively traversing the decision tree to find the class label 
    """
    if node.feat == -1:
        return node.getResult()

    for k, i in zip(kind[node.getFeat()], range(len(kind[node.getFeat()]))):

        if k == tuple[node.getFeat()]:
            ret = find_class_rec(node.getNext(i), kind, tuple)
            return ret

    return 'invalid'


"""

Main Program starts here

"""
# read arguments from command line:

train_data_file = sys.argv[1]
test_data_file = sys.argv[2]
result_output_file = sys.argv[3]

# open the input train file
with open(train_data_file, 'r') as f:
    # reading attributes
    attr = f.readline().split()
    attr_check_list = [False] * len(attr)  

    # DataBase to store the categories
    database = []
    kind = []  

    for line in f:
        category_list = line.split()
        for i, category in enumerate(category_list):

            kind_len = len(kind)
            attr_len = len(attr)

            if kind_len != attr_len:
                category_set = set()
                category_set.add(category)
                kind.append(category_set)
            else:
                kind[i].add(category)

        database.append(category_list)

decision_tree_root = set_criteria(database, attr, attr_check_list, kind)

with open(test_data_file, 'r') as f:
    test_attr = f.readline().split()
    test_prediction = []  # List to store results (predictions)
    test_db = [line.split() for line in f]

for tuple in test_db:
    test_prediction.append(find_class_rec(decision_tree_root, kind, tuple))

with open(result_output_file, 'w') as f:
    # Concatenate attributes into a header line
    attributes = ''
    for a, i in zip(attr, range(len(attr))):
        if i == (len(attr) - 1):
            attributes += a
        else:
            attributes += a + '\t'
    f.write(attributes + '\n')

    for tuple, i in zip(test_db, range(len(test_db))):
        tuple_line = ''

        for value, index in zip(tuple, range(len(tuple))):
            if index == (len(tuple) - 1):
                tuple_line += value + '\t' + test_prediction[i]
            else:
                tuple_line += value + '\t'


        f.write(tuple_line + '\n')
