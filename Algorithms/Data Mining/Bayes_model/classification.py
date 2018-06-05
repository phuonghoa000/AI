import arff
import math
import sys
import numpy as np

###
def read(data):    
    """
    Read file *.arff.
    
    Parameter
    -----------------
    data: string
        The name of the dataset file (training data or testing data)
    
    Returns
    -----------------
    dataset: list
        The data set.
    attributes: list
        The attributes of the data set.
    """
    # Read file *.arff and process
    dataset = arff.load(open(data, 'r'))
    attributes = dataset['attributes']
    dataset = dataset['data']
    
    return dataset, attributes

###
def learn(dataset, attributes):
    """
    Learning classification model based on the data set (dataset)
    and the attributes of the data set (attributes).
    
    Parameters
    -----------------
    dataset: list
        The data set.
    attributes: list
        The attributes of the data set.
    
    Return
    -----------------
    classifier_model: list
        The data classifier model.
    """
    #
    classifier_model = []
    len_at = len(attributes)
    
    # handle datasets
    for i in range(len_at - 1):
        # if the data is fragmented, with each attribute,
        # we find the frequency of occurrence of each different value of that attribute for each class
        # we use Laplacian correction to avoid conditional probability be zero.
        if type(attributes[i][1]) == type(classifier_model):
            temp = np.ones((len(attributes[i][1]) + 1, len(attributes[len_at - 1][1])))
            for j in range(len(dataset)):
                for k in range(len(attributes[i][1])):
                    check = False
                    for r in range(len(attributes[len_at - 1][1])):
                        if dataset[j][i] == attributes[i][1][k] and dataset[j][len_at - 1] == attributes[len_at - 1][1][r]:
                            temp[k][r] += 1
                            check = True
                            break
                    if check == True:
                        break
            
            for j in range(len(attributes[len_at - 1][1])):
                temp[len(attributes[i][1]), j] = sum(temp[0: len(attributes[i][1]), j: j + 1])
            classifier_model.append(temp)
        
        # if data is continuous, we find the expected value (mean) and standard deviation
        else:
            temp = np.zeros((3, len(attributes[len_at - 1][1])))
    
            # we find the expected value
            for j in range(len(dataset)):
                for k in range(len(attributes[len_at - 1][1])):
                    if dataset[j][len_at - 1] == attributes[len_at - 1][1][k]:
                        temp[0][k] += dataset[j][i]
                        temp[2][k] += 1
                        break
            for j in range(len(temp[0])):
                temp[0][j] = temp[0][j] / float(temp[2][j])
            
            # we find standard deviation                        
            for j in range(len(dataset)):
                for k in range(len(attributes[len_at - 1][1])):
                    if dataset[j][len_at - 1] == attributes[len_at - 1][1][k]:
                        temp[1][k] += (dataset[j][i] - temp[0][k]) ** 2
                        break
            for j in range(len(temp[0])):
                temp[1][j] = math.sqrt(temp[1][j] / float(temp[2][j]))
            
            classifier_model.append(temp)
     
    # we find the frequency of occurrence of each different value of attribute label
    # we use Laplacian correction to avoid conditional probability be zero
    temp = np.ones((2, (len(attributes[len_at - 1][1]))))
    for i in range(len(dataset)):
        for j in range(len(attributes[len_at - 1][1])):
            if dataset[i][len_at - 1] == attributes[len_at - 1][1][j]:
                temp[0][j] += 1
                break
    for i in range(len(attributes[len_at - 1][1])):
        temp[1][i] = len(dataset) + len(attributes[len_at - 1][1])
        
    classifier_model.append(temp)
    
    return classifier_model         

###
def _apply(dataset, attributes, model):
    """
    Apply classification model on the testing data set
    to predict the class for the samples in datasets.
    
    Parameters
    -----------------
    dataset: list
        The testing data set.
    attributes: list
        The attributes of the training data set.
    model: list
        The data classifier model.

    Return
    -----------------
    prediction: list
        The set of label corresponding to samples in the testing data set.
    """
    #
    prediction = []
    len_mod = len(model)
    
    # find label for each sample in the testing data set
    for i in range(len(dataset)):
        # find conditional probability for each attribute value of sample then multiply together
        prob = np.array([model[len_mod - 1][0][j] / model[len_mod - 1][1][j]
                         for j in range(len(model[len_mod - 1][0]))])
        for j in range(len_mod - 1):
            for k in range(len(prob)):
                # if data is fragmented
                if type(attributes[j][1]) == type(prediction):
                    for r in range(len(model[j]) - 1):
                        if dataset[i][j] == attributes[j][1][r]:
                            prob[k] = prob[k] * model[j][r][k] / model[j][len(model[j]) - 1][k]
                            break
                # if data is continuous, we computed based on Gaussian distribution
                else:
                    e = 2.718281828
                    pi = 3.141592654
                    f = e ** (-((dataset[i][j] - model[j][0][k]) ** 2) / 2 / (model[j][1][k] ** 2))
                    f /= (model[j][1][k] * math.sqrt(2 * pi))
                    prob[k] = prob[k] * f
        
        # find label that it has conditional probability maximum
        idx_max = 0
        for j in range(1, len(prob)):
            if (prob[j] > prob[idx_max]):
                idx_max = j
        
        prediction.append(attributes[len_mod - 1][1][idx_max])
    
    return prediction

###
def classify(train, test):
    dTrain, atTrain = read(train)
    dTest, _ = read(test)
    m = learn(dTrain, atTrain)
    lblTest = _apply(dTest, atTrain, m)  
    return lblTest

###
def main():
    train = sys.argv[1]
    test = sys.argv[2]
    result = classify(train, test)
    
    f = open(sys.argv[3], 'w')
    for i in range(len(result)):
        f.write(result[i])
        f.write('\n')
    f.close()
    
    return

###
main()