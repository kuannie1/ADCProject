"""
Compress an image and save it to a binary file
Main script that utilizes all other components:
    takes in image through command line args
    converts img from RGB to YCbCr colorspace
    following steps are done individually on all 3 color channels:
        split into blocks
        subtract 127 for each pixel value to center around 0
        (transform: DCT, DWT, etc)
        quantization (rounds numbers to ints and sets many vals to 0)
        huffman (find frequencies of pixel values and apply Huffman)
    stitch all blocks and color channels back together into one 3D matrix
    save the 3D matrix into a binary file

    possibility: call gnuradio from this script
"""
import numpy as np
import cv2
import image_processing
import frequency_calculator
import huffman
import data_processing

def main(img, header, fn='fileOutput.dat'):
    """ Creates final np array of -1s and 1s to be written to file"""

    # TODO add img processing stuff
    img_binary_array = []

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_binary_array.extend(data_processing.make_binary_list(img[i][j]))
    img_binary_array = np.array(img_binary_array) 

    write_to_file(img_binary_array, 'bin_array2_unencoded_y_tile.dat')
    freqs = frequency_calculator.get_frequencies(img)
    huff_tree = huffman.make_huffman_tree(freqs)  
    code_dict = huffman.code_from_tree(huff_tree) # dictionary {number: number}
    encoded_img, dimensions = huffman.encode_image(img, code_dict) 
    write_to_file(encoded_img, 'bin_array2_encoded_y_tile.dat')
    decode_dict = data_processing.flip_dictionary(code_dict) 
    print('DECODE DICT = ', decode_dict) 
    decode_dict = data_processing.dictionary_to_binary(decode_dict) 
    np.set_printoptions(threshold='nan')
    args = [header, dimensions, encoded_img, header, decode_dict, header]  
    # print('================')
    # print('ENCODED IMG DATA BITS')
    # print(encoded_img)
    print('================')
    print('dimensions=', dimensions)
    data = np.concatenate(args)
    print('================')
    print('TOTAL DATA LENGTH = ', len(data), ' BITS')
    print('================')
    data = data_processing.expand(data)
    data = data_processing.complexize_data(data)
    write_to_file(data, fn)

    return 
def write_to_file(complex_array, fn):
    """ Takes in np array with complex values & writes them to file """
    #source; https://stackoverflow.com/questions/29809988/numpy-array-tofile-binary-file-looks-strange-in-notepad
    print fn
    fp = open(fn, mode='wb')
    off = np.array(complex_array, dtype=np.float32)
    off.tofile(fp)
    fp.close()

    
if __name__ == '__main__':
    ImageProcessing = image_processing.ImageProcessing()
    ImageProcessing.compress()
    img = ImageProcessing.tiles[6].y_tile
    image_processing.save_image(img, 'images/img_precompressed.jpg')
    header = np.zeros(1000)
    header[41] = 1
    main(img, header, 'no_transmission.dat')
    