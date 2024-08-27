# python 2021034184_rana_hw1.py 10 input.txt output.txt

from itertools import combinations
import re
import sys

def percentage(cnt, total):
    """
    Calculates the percentage 
    """
    return (cnt / total) * 100

def subset_is_frequent(trs, arr) -> bool:
    '''
    Checks if all subsets of arr are frequent itemsets 
    '''
    for i in range(len(arr)):

        if i == 0:
            continue

        subsets = list(combinations(arr, i))
        for subset in subsets:

            s = list(subset)
            flag = False
            for l in trs[len(s)-1]:
                if set(s).issubset(set(l)):
                    flag = True

            if flag is False:
                return False

    return True

def generate_candidates(candidate_itemsets, trs, size) -> list:
    '''
    Returns a list of itemsets of given size that are frequent
    '''
    ret = list()

    cnt = 0
    for fir in range(len(candidate_itemsets)-1):
        cnt = cnt+1

        sec = fir + 1
        while True:

            if sec >= len(candidate_itemsets):
                break

            uni = set(candidate_itemsets[fir]) | set(candidate_itemsets[sec])

            if len(uni) == size+1 and subset_is_frequent(trs, list(uni)):
                ret.append(list(uni))

            sec = sec + 1

    return ret

if __name__ == "__main__":
    min_sup = float(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]


    # ---OPEN & READ---
    with open(input_file, 'r') as f:
        trs_data = []
        
        while True:
            line = f.readline()
            if not line:
                break
            
            numbers = re.findall(r'\d+', line)
            
            transaction = []
            for n in numbers:
                transaction.append(int(n))
            
            trs_data.append(transaction)

    candidate_itemsets = list()
    trs = list()
    cnt = list()  

    one_cnt = {}
    one_itemsets = set() # unique items

    # ---count---
    for ts in trs_data:
        for num in set(ts):  

            one_itemsets.add(num)  

            # increment OR initialize
            one_cnt[num] = one_cnt.get(num, 0) + 1

    one_list_items = list()

    tmp = list(one_itemsets) # temporarily list

    index = 0
    for t in tmp:
        support = one_cnt[t] * 100 / len(trs_data)  

        # threshold
        if support >= min_sup:
            one_list_items.append([t])

    candidate_itemsets.append(one_list_items)
    trs.append(one_list_items)

    list_one_cnt = []
    for num in one_list_items:
        list_one_cnt.append(one_cnt[num[0]])
    cnt.append(list_one_cnt)

    k = 0
    while True:

        if len(candidate_itemsets[k]) == 0 or len(trs[k]) == 0:
            break

        com = generate_candidates(candidate_itemsets[k], trs, k+1)
        candidate_itemsets.append(com)

        tmp_cnt = [0 for i in range(len(com))]
        index = 0
        
        # Count occurrences of each itemset in trs_data
        for index, itemset in enumerate(com):
            count = 0
            
            for tr in trs_data:
                if set(itemset).issubset(set(tr)):
                    count += 1  
            
            tmp_cnt[index] = count  

        cnt.append(tmp_cnt)

        tmp = []
        index = 0
        for sup in tmp_cnt:
            if (sup * 100 / len(trs_data)) >= min_sup:
                tmp.append(com[index])
            index = index + 1
        trs.append(tmp)
        k = k + 1

    # removing duplicates
    arr = []
    for tr_i in range(len(trs)):
        chk = {}
        tmp = []
        for j in range(len(trs[tr_i])):

            if j in chk:
                continue

            trs[tr_i][j].sort()
            tmp.append(trs[tr_i][j])

            for k in range(j+1, len(trs[tr_i])):
                if set(trs[tr_i][j]) == set(trs[tr_i][k]):
                    chk[k] = True

        arr.append(tmp)

    with open(output_file, 'w') as f:
        for r in range(len(arr)):
            for c in range(len(arr[r])):
                for row2 in range(len(arr)):
                    for c2 in range(len(arr[row2])):

                        if set(arr[r][c]).issubset(set(arr[row2][c2])) or set(arr[row2][c2]).issubset(set(arr[r][c])):
                            continue
                        
                        sup_cnt = 0
                        conf_cnt = 0
                        conf_all = 0

                        union_set = set(arr[r][c]).union(set(arr[row2][c2]))

                        for tr in trs_data:

                            tr_set = set(tr)
                            if union_set.issubset(tr_set):
                                sup_cnt = sup_cnt + 1
                                conf_cnt = conf_cnt + 1

                            if set(arr[r][c]).issubset(tr_set):
                                conf_all = conf_all + 1

                        if conf_cnt == 0 or conf_all == 0:
                            continue

                        open_b = '{'
                        close_b = '{'

                        index = 0
                        for r_item in arr[r][c]:
                            if index < len(arr[r][c])-1:
                                open_b += str(r_item) + ','
                            else:
                                open_b += str(r_item)
                            index = index + 1
                        open_b += '}'

                        index = 0
                        for item in arr[row2][c2]:
                            if index < len(arr[row2][c2])-1:
                                close_b += str(item) + ','
                            else:
                                close_b += str(item)
                            index = index + 1
                        close_b += '}'

                        sup = percentage(sup_cnt , len(trs_data))
                        conf = percentage(conf_cnt , conf_all)

                        if sup < min_sup:
                            continue

                        f.write("{}\t{}\t{:.2f}\t{:.2f}\n".format(open_b, close_b, sup, conf))
                        # print(sup_cnt)
