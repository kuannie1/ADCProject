"""
Script to take a compressed image saved as a binary file and retrieve the image

Steps:
    Unbinarize the file
    Puffman
    Unquantize
    Inverse DCT/inverse transform
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


def main(readfilename, header, transmitted=True,
    writefilename='images/decompressed_img.jpg', start_index = 0, end_index = 0):
    """ Recreates image from transmitted data """

    data = read_from_file(readfilename)
    data = data_processing.decomplexize_data(data)
    print('decomplexized')
    if end_index != 0:
        data = data[start_index:end_index]
    if transmitted:
        data = data_processing.estimate_transmitted_signal(data)
    else:
        data = np.real(data)
    print('estimated transmitted signal')
    data = data_processing.unexpand_and_correct(data)
    print('unexpanded')
    [dimensions, encoded_img, decode_dict] = data_processing.data_from_array(data, header)
    print('data to array')
    decode_dict = data_processing.binary_to_dictionary(decode_dict)
    img_1d = puffman.puffman(encoded_img, decode_dict)
    print('LEN decoded img', len(img_1d))
    img = puffman.to_array(img_1d, dimensions)
    image_processing.save_image(img, writefilename)
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
    header = np.zeros(1000)
    header[41] = 1
    main('no_transmission.dat', header, transmitted=False)