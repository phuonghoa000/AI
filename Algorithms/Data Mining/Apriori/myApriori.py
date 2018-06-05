import numpy as np
import sys

def sub_array_gen(lst, n_element):
    sub_arr = []                                                    # Initiate subset list
    for i in range(0, len(lst)):
        # Add subset to subset list when i + n_element is not out of lst's range
        if i + n_element <= len(lst):
            sub_arr.append(lst[i: i + n_element])
        # Add subset to subset list when i + n_element is out of lst's range
        else:
            temp = []                                               # Initiate subset
            temp.extend(lst[i: i + n_element])                      # Add elements within range to subset
            missing = n_element - len(temp)                         # Find the number of missing item in subset
            temp.extend(lst[0: missing])                            # Add items from the beginning of lst
            temp.sort()                                             # Sort subset before add to subset list
            sub_arr.append(temp)                                    # Add to subset list
    return sub_arr


# candidate_gen(freq_set): Generate candidate set C(k) (cand_set) from frequent item sets F(k - 1) (freq_set)
def candidate_gen(freq_set):
    freq_set.sort()                                                 # Sort item sets in lexicographic order
    cand_set = []                                                   # Initiate candidate set as NULL
    freq_set_size = len(freq_set)                                   # Get number of frequent item sets
    item_set_size = len(freq_set[0])                                # Get number of items within a frequent item set

    # Joining step:
    # Find all pairs of frequent item sets that differ only in the last item
    for i in range(0, freq_set_size - 1):                           # Select first item set for comparison
        c = []                                                      # Initiate a new item set c
        for j in range(i + 1, freq_set_size):                       # Select second item set for comparison
            # Select items exist in 1 item set but not in the other
            last_el_1 = list(set(freq_set[i]) - set(freq_set[j]))
            last_el_2 = list(set(freq_set[j]) - set(freq_set[i]))

            # Check if selected item sets differ only in the last item
            if len(last_el_1) == len(last_el_2) == 1:
                # Check if the different items are the last items of selected item sets
                idx_1 = freq_set[i].index(last_el_1[0])
                idx_2 = freq_set[j].index(last_el_2[0])
                if idx_1 == idx_2 == item_set_size - 1:
                    c = freq_set[i][:]                              # Copy the first item set to c
                    c.extend(last_el_1 if last_el_1 > last_el_2 else last_el_2)     # Join 2 item sets
                    cand_set.append(c)                              # Add c to C(k)
                else:
                    continue
                # Pruning step:
                sub_set = sub_array_gen(cand_set[len(cand_set) - 1], len(cand_set[len(cand_set) - 1]) - 1)
                # Find subsets of c in F(k - 1)
                for k in range(0, len(sub_set)):
                    if sub_set[k] not in freq_set:
                        del cand_set[len(cand_set) - 1]
                        break
            else:
                continue
    return cand_set

# Read data form file_name
def read_file(file_name):
    in_data = []
    f = open(file_name, 'r')
    
    while True:
        temp_lst = f.readline().split()
        if not temp_lst != []:
            break
        in_data.append(temp_lst)
    f.close()
    
    # convert each element from string to int
    for i in range(0, len(in_data)):
        in_data[i] = map(lambda x: int(x), in_data[i])
        
    return in_data

# Write the result to file_name
def write_file(file_name, out_data):
    f = open(file_name, 'w')
    
    for i in range(0, len(out_data)):
        # convert each element of list from int (or float) to string
        for j in range(0, len(out_data[i])):
            out_data[i][j] = str(out_data[i][j])
        # format string
        s = ' '.join(out_data[i])
        f.writelines(s)
        f.write("\n")
    f.close()
    
    return

# Find index of value in the list, if the value does not exist, the result returned is -1
def is_same(li, value):
    for i in range(0, len(li)):
        if value == li[i]:
            return i
    return -1

# Initialize function arising candidates C(1)
def init_pass_C(_T):
    
    # inits candidates
    items = []
    for i in range(0, len(_T[0])):
        items.append(_T[0][i])
    
    # count the number of occurrences of each element in the items
    items_count = [1] * len(items)
    
    # browse database T and update items list and items_count list
    for i in range(1, len(_T)):
        for j in range (0, len(_T[i])):
            check = is_same(items, _T[i][j])
            if  check == -1:
                items.append(_T[i][j])
                items_count.append(1)
            else:
                items_count[check] += 1
   
    # find support of each element of items
    for i in range(0, len(items_count)):
        items_count[i] = (float)(items_count[i])/len(_T)
    
    # merge items and items_count into one and transpose
    C = np.array([items_count, items]).T
    
    return C

# Initialize function to find frequent item sets F(1)
def init_F1(C, mins):
    
    # comparing support of each candidates with minsup to create frequent item sets F(1)
    F = []
    for i in range(0, len(C)):
        if (C[i][0] >= mins):
            F.append(C[i])
            
    # convert F to list (not numpy.ndarray)
    for i in range(0, len(F)):
        F[i] = list(F[i])
    
    return F

# Find support of each candidates with database T
def sup_c_in_T(_c, T):
    count = 0
    for i in range(0, len(T)):
        check = 1
        for j in range(0, len(_c)):
            if is_same(T[i], _c[j]) == -1:
                check = 0
                break
        if check == 1:
            count += 1

    return count/(float)(len(T))

# Apriori algorithm
def alg_Apriori(T, mins):
    
    # init C(1) and F(1)
    C = init_pass_C(T)
    result = init_F1(C, mins)    
    F = []
    for i in range(0, len(result)):
        F.append(result[i][1:len(result[i])])
    
    
    while (len(F) > 0):
        # update C(K) from F(k - 1)
        C = candidate_gen(F)
        F = []
       
        # scan the data and update result
        carry = len(result)
        for i in range(0, len(C)):
            sup_c = sup_c_in_T(C[i], T)
            if sup_c >= mins:
                result.append(C[i])
                result[len(result) - 1].insert(0, sup_c)
        
        # update F(k - 1)
        for i in range(carry, len(result)):
            F.append(result[i][1:len(result[i])])
            
    return result

# Reformat the datatype of result
def format_result(result):
    for i in range(0, len(result)):
        result[i][0] = (round)(result[i][0], 2)
        for j in range(1, len(result[i])):
            result[i][j] = (int)(result[i][j])
    return result

# main
def main():
    T = read_file(sys.argv[1])
    re = alg_Apriori(T, (float)(sys.argv[3]))
    re = format_result(re)
    write_file(sys.argv[2], re)
    return

main()