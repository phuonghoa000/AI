import neural_nets as nets
import mnist
import sys
from scipy.misc import imread
import numpy as np

def convert_to_list(s):
    s = s.replace('[', '')
    s = s.replace(']', '')
    l = s.split(',')
    l = [int(i) for i in l]
    
    return l
	
def main():
    type = sys.argv[1]
    li = convert_to_list(sys.argv[2])
    li[-1] = 10
    epoch = int(sys.argv[3])
    lrate = float(sys.argv[4])

    if (type == '1'):
        img_name = sys.argv[5]
        img = imread(img_name)
        img = np.reshape(img, (28*28, 1))

        print 'loading...'
        li[0] = img.size
        training_data = mnist.load_data('data/train_images.idx3-ubyte', 'data/train_labels.idx1-ubyte', 'rb', 60000, 1)
        net = nets.Neural_nets(li)
        print 'training...'
        net.training_model(training_data, epoch, lrate)
        val = np.argmax(net.learning_model(img))

        print 'The number is %d.' % (val)

    else:
        print 'loading...'
        li[0] = 784
        training_data = mnist.load_data('data/train_images.idx3-ubyte', 'data/train_labels.idx1-ubyte', 'rb', 60000, 1)
        test_data = mnist.load_data('data/test_images.idx3-ubyte', 'data/test_labels.idx1-ubyte', 'rb', 10000, 0)
        net = nets.Neural_nets(li)
        print 'training...'
        net.training_model(training_data, epoch, lrate, test_data)
        
main()