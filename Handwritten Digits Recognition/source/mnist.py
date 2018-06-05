import numpy as np
import struct

def format_output(number):
    """Convert a number to a bool array with element has index is 'number' has value is 1, another is 0. """
    out = np.zeros(shape = (10, 1))
    out[number] = True
    
    return out
	
def load_data(data_name, label_name, _type, size, sign):
    
    sz = 28 * 28
    ##########################################
    # load label of data
    # it 's the correct output of image data
    f = open(label_name, _type)
    f.seek(8)
  
    labels = []
    
    if not sign:
        for i in range(size):
            val = f.read(1)
            val = struct.unpack('>B', val)
            labels.append(val[0])
    else:
        for i in range(size):
            val = f.read(1)
            val = struct.unpack('>B', val)
            val = format_output(val[0])
            labels.append(val)
    
    f.close()
    ##########################################
    # load image data
    # each image will be convert to a vector has 784 dimension
    f = open(data_name, _type)
    f.seek(16)

    data = []
    
    for i in range(size):
        img = np.ndarray(shape = (sz, 1))
        for j in range(i * sz, (i + 1) * sz):
            val = f.read(1)
            val = struct.unpack('>B', val)
            img[j - i * sz] = float(val[0])/255

        data.append(img)
        
    f.close()
    load_data = [(x, y) for x, y in zip(data, labels)]
    
    return load_data