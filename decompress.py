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

def main(filename):
    """ Recreates image from transmitted data """

    # Will need to retreive image data (dimensions, encoded img, dictionary) for each tile of each channel of the image

    data = read_from_file(filename) # I don't think this will work because read_from_file doesn't return anything???
    #data = decomplexize data
    # data = # thing to remove noise before and after transmitted signal 
    data = data_processing.unexpand_and_correct(data)
    # [dimensions, encoded_img, decode_dict] = result of function that pulls these from data
    decode_dict = data_processing.binary_to_dictionary(decode_dict)

    img_1d = puffman.puffman(encoded_img, decode_dict)
    #img = puffman.to_array(img_1d, dimensions)

    #img processing stuff

    #cv img np array to img file export

def read_from_file(filename):
    fileobj2 = open(filename, mode='rb')
    off = np.fromfile(fileobj2, dtype = np.float32)
    print(off)
    fileobj2.close()
    return off

if __name__ == '__main__':
	y = read_from_file('transmissiontest.dat')
	y = data_processing.decomplexize_data(y)
        y = y[252800 + 30-1 : 252800 + 612-1]
 	y = data_processing.estimate_transmitted_signal(y)
 	y = data_processing.unexpand_and_correct(y)
        np.set_printoptions(threshold='nan')
 	print y
