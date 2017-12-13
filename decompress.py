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



def main(filename, header, start_index = 0, end_index = None):
    """ Recreates image from transmitted data """

    # Will need to retreive image data (dimensions, encoded img, dictionary) for each tile of each channel of the image

    data = read_from_file(filename)
    if end_index == None: end_index = len(data)
    data = dataprocessing.decomplexize(data)
    data = data[start_index:end_index]
    data = data_processing.unexpand_and_correct(data)
    [dimensions, encoded_img, decode_dict] = data_processing.data_from_array(data, header)
    decode_dict = data_processing.binary_to_dictionary(decode_dict)
    img_1d = puffman.puffman(encoded_img, decode_dict)
    img = puffman.to_array(img_1d, dimensions)
    image_processing.save_image(img)

def read_from_file(filename):
    fileobj2 = open(filename, mode='rb')
    off = np.fromfile(fileobj2, dtype = np.float32)
    fileobj2.close()
    return off

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

