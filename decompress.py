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
#from find_start_end_signal import *



def main(filename, header, start_index = 0, end_index = 0):
    """ Recreates image from transmitted data """

    data = read_from_file(filename)
    data = data_processing.decomplexize_data(data)
    print('decomplexized')
    if end_index != 0:
        data = data[start_index:end_index]
    data = data_processing.estimate_transmitted_signal(data)
    print('estimated transmitted signal')
    data = data_processing.unexpand_and_correct(data)
    print('unexpanded')
    [dimensions, encoded_img, decode_dict] = data_processing.data_from_array(data, header)
    print('data to array')
    np.set_printoptions(threshold='nan')
    decode_dict = data_processing.binary_to_dictionary(decode_dict)
    print('decode_dict')
    img_1d = puffman.puffman(encoded_img, decode_dict)
    print('len_1d_img =', len(img_1d))
    print('dimensions =', dimensions)
    img = puffman.to_array(img_1d, dimensions)

    image_processing.save_image(img, 'super_decompressed_doge.jpg')

    print 'done'
    return [decode_dict, img]

def read_from_file(filename):
    fileobj2 = open(filename, mode='rb')
    off = np.fromfile(fileobj2, dtype = np.float32)
    fileobj2.close()
    return off


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
	header = np.zeros(200)
	header[41] = 1
	main('receivedDoge.dat', header, start_index=1156245, end_index=6949292)
