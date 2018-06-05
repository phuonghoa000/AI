# candidateGen.py

# Input: File contains item sets. Each item set is on a single line and every item in item set is separated by ' '.
# Output: File contains candidate set. Content is the same as input.

import sys


# Function sub_array_gen(lst, n_element)(Auxiliary function): Generate all subsets with len(lst) - 1 elements of lst
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


def main():
    freq_set = []
    f = open(sys.argv[1], "r")
    while True:
        temp_lst = f.readline().split()
        if not temp_lst != []:
            break
        freq_set.append(temp_lst)
    f.close()

    cand_set = candidate_gen(freq_set)

    f = open(sys.argv[2], "w")
    for i in range(0, len(cand_set)):
        str = ' '.join(cand_set[i])
        f.writelines(str)
        f.write("\n")
    f.close()

main()