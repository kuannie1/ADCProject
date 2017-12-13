"""
Script to take a compressed image saved as a binary file and retrieve the image

Steps:
    Unbinarize the file
    Puffman
    Unquantize
    Inverse DCT/inverse transform
    Add 127 to each element in each block
    Stitch back the blocks
    convert back to RGB
    save as img
"""

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import data_processing
import puffman
import image_processing
from find_start_end_signal import *



def main(filename, header, start_index = 0, end_index = 0):
    """ Recreates image from transmitted data """

    data = read_from_file(filename)
    data = data_processing.decomplexize_data(data)
    data = np.real(data)
    if end_index != 0:
	    data = data[start_index:end_index]
    data = data_processing.unexpand_and_correct(data)
    [dimensions, encoded_img, decode_dict] = data_processing.data_from_array(data, header)
    np.set_printoptions(threshold='nan')
    decode_dict = data_processing.binary_to_dictionary(decode_dict)
    img_1d = puffman.puffman(encoded_img, decode_dict)
    print('len_1d_img =', len(img_1d))
    print('dimensions =', dimensions)
    img = puffman.to_array(img_1d, dimensions)

    image_processing.save_image(img)

    print 'done'
    return [decode_dict, img]

def read_from_file(filename):
    fileobj2 = open(filename, mode='rb')
    off = np.fromfile(fileobj2, dtype = np.float32)
    fileobj2.close()
    return off

<<<<<<< HEAD
<<<<<<< HEAD

def compare_rx_tx(received, original):
    size = received.size
    if (received.size != original.size):
        print "sizes are different"
        if (received.size>original.size):
            size = original.size 
    # use logical xor to compare received & original vectors of length size
    xor_rx_tx = np.logical_xor(received[0:size], original[0:size])
    print np.invert( xor_rx_tx )

=======
=======
>>>>>>> 32ab80b5a1049519fda7702d891c1785131daf34

def compare_rx_tx(received, original):
    size = received.size
    if (received.size != original.size):
        print "sizes are different"
        if (received.size>original.size):
            size = original.size 
    # use logical xor to compare received & original vectors of length size
    xor_rx_tx = np.logical_xor(received[0:size], original[0:size])
    print np.invert( xor_rx_tx )


if __name__ == '__main__':
    
    y = read_from_file('sixtythousandbits.dat')
    y = data_processing.decomplexize_data(y)
    y = y[1076851+3031-1:4079857-1]
    print len(y)
    #y = y[1634000+332 - 1:1634000+3314 - 1]
    #y = y[252800 + 30-1 : 252800 + 612-1]
    y = data_processing.estimate_transmitted_signal(y)
    plt.plot(y)
    plt.show()
    y = data_processing.unexpand_and_correct(y)
    np.set_printoptions(threshold='nan')
    print y
    print len(y)
    
    """
    y = read_from_file('sixtythousandbits.dat')
    (start_i, end_i) = find_start_end_signal('sixtythousandbits.dat')
    y = data_processing.decomplexize_data(y)
    y = y[start_i:end_i]
        #y = y[1634000+332 - 1:1634000+3314 - 1]
        #y = y[252800 + 30-1 : 252800 + 612-1]
    y = data_processing.estimate_transmitted_signal(y)
    plt.plot(y)
    plt.show()
    """

if __name__ == '__main__':
	header = np.zeros(200)
	header[41] = 1
	main('notransmission.dat', header)
