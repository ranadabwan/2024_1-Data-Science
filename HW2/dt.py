#python dt.py dt_train.txt dt_test.txt dt_rest1.txt4

import sys
import math


class TreeNode:

    """
    A node on decision tree
    """

    def __init__(self,feat):
        self.feat = feat
        self.next = []
        self.result = 'invalid'


    def append(self. newNode):
        self.next.append(newNode)

    def setFeat(self, feat):
        self.feat = feat

    def setResult(self, result):
        self.result = result
    
    def getNext(self, index):
        return self.next[index]
    
    def getResult(self):
        return self.result
    
    def InfoGain(values):

        #caculates the entropy of a given list

        sum = 0
        ret = 0.0


        for v in values:
            sum = sum + v

        for x in values:
            if x == 0 or sum == 0:
                continue

            p = x / sum
            ret = ret - p * math.log2(p)

        return ret
    

def DomainCnt(DB, kind, n):

    #Calculates the frequesncy of each attribute

    ret = [0 for i in range(len(kind[n]))]
    domain_idx = {}

    i = 0
    for k in kind[n]:
        domain_idx[k] = i
        i = i + 1

    for tuple in DB:
        ret[domain_idx[tuple[n]]] = ret[domain_idx[tuple[n]]] + 1

    return ret

def setCriteria(DB, attr, attr_chk, kind):
    #Recursively bui;ding the desicion tree

    ret = TreeNode(-1)

    #InfoGain(D)
    ret_cnt = DomainCnt(DB, kind, -1)
    all_info = InfoGain(ret_cnt)

    if all_info == 0:
        ret.setResult(DB[0][-1])
        return ret
    gain_list = []
    for a in range(len(attr)-1):

        if attr_chk[a] == True:
            gain_list.append(-123456789)
            continue

        info_a = 0.0
        for k in kind[a]:

            idx = 0
            ret_domain = {}
            cond_cnt = [0 for i in range(len(kind[-1]))]

            for tuple in DB:
                if tuple[a] != k:
                    continue

                if tuple[-1] not in ret_domain:
                    ret_domain[tuple[-1]] = idx
                    cond_cnt[idx] = cond_cnt[idx] + 1
                    idx = idx + 1
                else:
                    cond_cnt[ret_domain[tuple[-1]]] = cond_cnt[ret_domain[tuple[-1]]] + 1


                info_a_k = InfoGain(cond_cnt)
                info_a = info_a + sum(cond_cnt) / len(DB) * info_a_k

            gain_a = all_info = info_a
            gain_list.append(gain_a)


        max_gain_idx = gain_list.index(max(gain_list))
        ret.setFeat(max_gain_idx)



        dc = DomainCnt(DB, kind, -1)
        max_dc_idx = dc.index(max(dc))
        max_label = list(kind[-1])[max_dc_idx]

        for k, i in zip(kind[max_gain_idx]m range(len(kind[max_gain_idx]))):
        
        newDB = []
        for tuple in DB:
            if tuple[max_gain_idx] == k:
                newDB.append(tuple)


            if len(newDB) == 0:
                newNode = TreeNode(-1)
                newNode.setResult(max_label)
                ret.append(newNode)
                continue

            new_attr_chk = attr_chk.copy()
            new_attr_chk[max_gain_idx] = True

            subNode = setCriteria(newDB, attr, new_attr_chk, kind)
            ret.append(subNode)

            return ret
        

def SearchResult(node, kind, tuple):


    #Rec traversing the decision tree to find the class label


    if node.feat == -1:
        return node.getResult()
        
    for k, i in zip(kind[node.getFeat()], range(len(kind[node.getFeat()]))):

        if k == tuple[node.getFeat()]:
            ret = SearchResult(node.getNext(i), kind, tuple)
            return ret
        return 'invalid'
    

    #Main


    input_train = sys.argv[1]
    input_test = sys.argv[2]
    output_name = sys.argv[3]



    f = open(input_train, 'r')


    attr = f.readline().split()
    attr_chk = [False for i in range(len(attr))]


    DB = []
    kind = []


    while True:

        line = f.readline()
        if not line:
            break

    category_list = line.split()
    category_idx = {}
    category_cnt = 0


    for i, category in zip(range(len(category_list)), category_list):
        if len(kind) != len(attr):
            category_set = set()
            category_set.add(category)
            kind.append(category_set)
        else:
            kind[i].add(category)

    DB.append(category_list)  


f.close()

dt_root = setCriteria(DB, attr, attr_chk,kind)
test_attr = f.readline().split()
TDB =[]
test_result = []


while True:



    line = f.readline()
    if not line:
        break
    TDB.append(line.split())


f.close


for tuple in TDB:

    test_result.append(SearchResult(dt_root, kind, tuple))

f = open(output_name, 'w')


attrs = ''
for a, i in zip(attr, range(len(attr))):
    if i == (len(attr)-1):
        attrs = attrs + a
    else:
        attrs = attrs + a + '\t'
    f.write(attrs + '\n')


    for tuple, i in zip(tuple, range(len(tuple))):
        if j == (len(tuple)-1):
            tuple_line = tuple_line + v + '\t' + test_result[i]
        else:
            tuple_line = tuple_line + v + '\t'

    f.write(tuple_line + '\t')

f.close()                            