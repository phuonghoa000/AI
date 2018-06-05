# mykmeans.py

import sys
import math
import random as rand


# File input/output:
def fread(fname):                            # Read data fom file
    att_types = []
    data = []
    file = open(fname, 'r')

    att_names = file.readline().strip().split(',')
    while True:
        line = file.readline()
        if line == '':
            break
        data.append(convert_dat(line.strip().split(',')))

    # Check data types:
    for i in range(0, len(data)):
        if len(att_types) != 0 and ' ' not in att_types:
            break
        for j in range(0, len(data[0])):
            att_types.append(get_type(data[i][j]))

    return att_names, att_types, data


def fwrite(att_names, clusters, fname):         # Write results to file
    file = open(fname, 'w')
    for i in range(0, len(att_names)):          # Write attribute's names to file
        file.write(att_names[i])
        file.write(',')
    file.write('Cluster\n')

    for i in range(0, len(clusters)):
        for j in range(0, len(clusters[i])):
            for k in range(0, len(att_names)):
                file.write(str(clusters[i][j][k]))
                file.write(',')
            file.write(str(i))
            file.write('\n')


# File input/output


# Calculations:
def cent_gen(k_number, _seed, in_data):            # Generate different centers for clusters randomly
    rand.seed(_seed)
    k_list = []
    data = []

    # Create new dataset from in_data with no repeated data with different names to avoid creating emoty cluster
    for i in range(0, len(in_data)):                # Remove first attribute
        data.append(in_data[i][1:])

    for i in range(0, len(data)):                   # Convert data to tuple
        data[i] = tuple(data[i])

    data = list(set(data))                          # Remove duplicates
    dat_list = rand.sample(data, k_number)          # Choose randomly k_number items from data

    num_list = []
    for i in range(0, len(dat_list)):               # Choose k from dat_list
        for j in range(0, len(in_data)):
            if list(dat_list[i]) == in_data[j][1:]:
                k_list.append(in_data[j])
                break

    return k_list


def find_cent(cluster, att_types):              # Find new centers for clusters
    new_cent = []
    for j in range(0, len(att_types)):
        if att_types[j].lower() == 'nominal' or att_types[j] == ' ':
            new_cent.extend(' ')
            continue
        temp = 0
        for i in range(0, len(cluster)):
            temp += cluster[i][j]
        new_cent.extend([float(temp) / len(cluster)])

    return new_cent


def SSE_cal(clusters, k_list, att_types):           # Calculate SSE
    SSE = 0
    for i in range(0, len(clusters)):
        for j in range(0, len(clusters[i])):
            SSE += (Euclid_dist(clusters[i][j], k_list[i], att_types)) ** 2

    return SSE
# Calculations


# Similarity Test:
# Euclidean Distance:
def Euclid_dist(p1, p2, att_types):
    if p1 == p2:
        return 0
    size = len(p1)
    dist = 0
    for i in range(0, size):
        if att_types[i].lower() == 'nominal':
            continue
        dist += (p1[i] - p2[i]) ** 2

    return math.sqrt(float(dist))


# Manhattan Distance:
def Man_dist(p1, p2, att_types):
    if p1 == p2:
        return 0
    size = len(p1)
    dist = 0
    for i in range(0, size):
        if att_types[i].lower() == 'nominal':
            continue
        dist += math.fabs(p1[i] - p2[i])

    return dist


# Cosine Similarity:
def Cos_sim(vect1, vect2, att_types):
    num = 0
    temp1 = 0
    temp2 = 0

    for i in range(0, len(vect1)):
        if att_types[i].lower() == 'nominal':
            continue
        num += vect1[i] * vect2[i]                  # Calculate vect1 * vect2
        temp1 += vect1[i] ** 2                      # Calculate Sum(vect1 ^ 2)
        temp2 += vect2[i] ** 2                      # Calculate Sum(vect2 ^ 2)

    vect1_abs = math.sqrt(temp1)                    # Calculate |vect1|
    vect2_abs = math.sqrt(temp2)                    # Calculate |vect2|

    return 1 - (num / (vect1_abs * vect2_abs))      # Calculate distance based on cosine similarity
# Similarity Test


# k-mean algorithm:
def k_mean(k_number, _seed, data, att_types, dist):
    k_list = cent_gen(k_number, _seed, data)

    clusters_old = []
    while True:
        # Initiate clusters:
        clusters = []
        for i in range(0, k_number):
            clusters.append([])

        # Clusterization:
        for i in range(0, len(data)):
            # Calculate similarities of current data and the first center:
            min_dist = dist(data[i], k_list[0], att_types)
            min_pos = 0
            for j in range(1, len(k_list)):
                # Calculate similarities of current data and the current center to find the most similar pair:
                temp_dist = dist(data[i], k_list[j], att_types)
                if min_dist > temp_dist:
                    min_dist = temp_dist
                    min_pos = j
            # Put data into right cluster based on above calculation:
            if min_dist == 0 and len(clusters[min_pos]) != 0:
                temp = clusters[min_pos][0]
                clusters[min_pos][0] = data[i]
                clusters[min_pos].extend([temp])
            else:
                clusters[min_pos].extend([data[i]])

        # Find new centers for clusters:
        k_list = []
        for i in range(0, len(clusters)):
            k_list.append(find_cent(clusters[i], att_types))

        if clusters == clusters_old:
            return clusters, k_list
        clusters_old = clusters


# Misc Functions:
def get_type(str):                  # Find type of given string
    if str == ' ' or str == '?':
        return ' '
    try:
        int(str)
        return 'numeric'
    except ValueError:
        try:
            float(str)
            return 'numeric'
        except ValueError:
            return 'nominal'


def convert_dat(data):                      # Convert data from string
    for i in range(0, len(data)):
        if data[i] == ' ' or str == '?':
            continue
        try:
            data[i] = int(data[i])
        except ValueError:
            try:
                data[i] = float(data[i])
            except ValueError:
                continue
    return data
# Misc Functions

def main():
    in_name = sys.argv[1]
    out_name = sys.argv[2]
    k_num = int(sys.argv[3])
    _seed = int(sys.argv[4])
    opt = int(sys.argv[5])

    names, types, data = fread(in_name)         # Read file
    if opt == 1:                                # Clustering with Euclidean distance
        clusters, k_list = k_mean(k_num, _seed, data, types, Euclid_dist)
    elif opt == 2:                              # Clustering with Manhattan distance
        clusters, k_list = k_mean(k_num, _seed, data, types, Man_dist)
    elif opt == 3:                              # Clustering with Cosine similarity
        clusters, k_list = k_mean(k_num, _seed, data, types, Cos_sim)
    else:
        return -1                               # Returns error

    fwrite(names, clusters, out_name)           # Write result to file

    SSE = SSE_cal(clusters, k_list, types)      # Calculate SSE
    print('SSE = %.2f' % SSE)
    return 0

main()