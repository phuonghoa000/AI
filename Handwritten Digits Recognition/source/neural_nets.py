import numpy as np
import random
import mnist # the library mnist to load mnist database (training data and test data)

# The class Neural_nets include functions to solve the recognize handwriting digits problem.
# It has 4 attributes consist of:
#     layers: number of layers of network.
#     sz: size of each layers (number neural of each layers of the network).
#     biases: the list of matrix bias values
#     weights: the list of matrix weight values
class Neural_nets(object):
    def __init__(self, sz):
        """ Initialize network's attributes"""
        self.layers = len(sz)
        self.sz = sz
        # random value in biases and weights
        # with mean is 0 and std is 1
        self.biases = [np.random.randn(n, 1) for n in sz[1:]]
        self.weights = [np.random.randn(n, m) 
                        for m, n in zip(sz[:-1], sz[1:])]
        
    def training_model(self, training_data, epoch, lrate, test_data = None):
        """ The training model train training_data with different parameters
            to figure out the best matrix of biases and weights.
            
        Parameters:
        training_data: The set of sample data with correct output.
        epoch: the loop number to train data
        lrate: learning rate
        test_data: The set of data is need to test to check network's ability.
        """
        n = len(training_data)
        mini_sz = 10
        cur_prop = 0
        current_weights = self.weights
        current_biases = self.biases
        li = []
        
        # With each epoch, convert position of every element in training_data
        # split training_data into set with small size, this help to save time to train.
        # We'll train with each set.
        # With each element in set, we call mini_training_model to train with set has size smaller.
        # After taking the result of mini_training_model, update biases and weigths.
        for i in range(epoch):
            random.shuffle(training_data)
            _set = [training_data[j:j+mini_sz] for j in range(0, n, mini_sz)]
         
            for mini_set in _set:
                new_b, new_w = self.mini_training_model(mini_set)
                self.biases = [b-(lrate/mini_sz)*nb for b, nb in zip(self.biases, new_b)]
                self.weights = [w-(lrate/mini_sz)*nw for w, nw in zip(self.weights, new_w)]
                
            # just write result if has test_data
            if test_data:
                re = self.result(test_data)
                _sum = len(test_data)
                new_prop = float(re) / _sum

                print 'Epoch #%d: %d / %d.' % (i, re, _sum)

                if (new_prop > cur_prop):
                    current_weights = self.weights
                    current_biases = self.biases
                    cur_prop = new_prop
                    li = [i, re, _sum]

        if test_data:
            self.weights = current_weights
            self.biases = current_biases
            print '-' * 20
            print 'Best epoch #%d: %d / %d.' % (li[0], li[1], li[2])
            print 'Best performance: %.2f%%.' % (cur_prop * 100)

            
    def mini_training_model(self, mini_set):
        """ The fuction train with a small size set."""
        
        # Initialize list of matrix new_b and new_w with all values is zero
        # these matrix's shape same to biases's shape and weights's shape
        new_b = [np.zeros(b.shape) for b in self.biases]
        new_w = [np.zeros(w.shape) for w in self.weights]
        
        # Train directly to input sample data with backpropagation function
        # Update new_b and new_w when receice result from that call function
        for x, y in mini_set:
            delta_b, delta_w = self.backpropagation(x, y)
            new_b =[b+db for b, db in zip(new_b,delta_b)]
            new_w =[w+dw for w, dw in zip(new_w,delta_w)]

        return (new_b, new_w)
            
    def learning_model(self, _input):
        """ This function just learn from trained data."""
        
        # with current biases and weights,
        # learn to figure out the output
        # the output is sigmoid(w.x + b)
        # with x is output of the previous's layer
        for b, w in zip(self.biases, self.weights):
            out = sigmoid(np.dot(w, _input) + b)
            _input = out
            
        return out
        
    def result(self, test_data):
        """ Result of test data.
            This function is compare the correct output y of input x
            and result of learning_model function with input is x.
            The result is sum of the correct predict times."""
        
        test_results = [int(np.argmax(self.learning_model(x)) == y)
                        for (x, y) in test_data]
        return sum(test_results)
            
    def backpropagation(self, x, y):
        """ The backpropagation algorithm.
        Parameters:
        x:  input of network
            is a vector has 784 dimension
        y:  input of network
            correct output of training sample
            is a vector has 10 dimension
            
        Returns:
        init_b: list of matrix biases, it's shape is coresponding to self.biases
        init_w: list of matrix weights, it's shape is coresponding to self.weights
        
        """
        
        # 'starting step'
        # initialize two variable is relate to biases and weights
        init_b = [np.zeros(b.shape) for b in self.biases]
        init_w = [np.zeros(w.shape) for w in self.weights]
        
        # 1. Feedforward
        # compute cost function (w.x + b) and output (same y)
        li_out = [x]
        li_z = []
        for i in range(1, self.layers):
            b = self.biases[i - 1]
            w = self.weights[i - 1]
            z = np.dot(w, li_out[-1]) + b
            out = sigmoid(z)
            li_out.append(out)
            li_z.append(z)      
        
        # 2. Output error
        # compute the error of the end layer of network
        error = (li_out[-1] - y)*sigmoid_derivation(li_z[-1])
       
        # 3. Backpropagate the error
        for i in range(1, self.layers):
            init_b[-i] = error
            init_w[-i] = np.dot(error, li_out[-i-1].T)
            if i == self.layers - 1:
                break
            z = li_z[-i-1]
            out = sigmoid_derivation(z)
            error = np.dot(self.weights[-i].T, error) * out
            
        return (init_b, init_w)
        
    
    
#############################################
# Some different function that is not in class Neural_nets
# but be need and relate to program's purpose

def sigmoid(val):
    """ Sigmoid function. """
    sigm = 1.0/(1.0+np.exp(-val))
    return sigm


def sigmoid_derivation(val):
    """ The derivative of sigmoid function."""
    dsigm = sigmoid(val)*(1.0-sigmoid(val))
    return dsigm