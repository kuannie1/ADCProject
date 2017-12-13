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

def main(img):
    """ Creates final np array of -1s and 1s to be written to file"""

    # TODO add img processing stuff

    freqs = frequency_calculator.get_frequencies(img)
    huff_tree = huffman.make_huffman_tree(freqs)
    

    code_dict = huffman.code_from_tree(huff_tree) # dictionary {number: number}
    encoded_img, dimensions = huffman.encode_image(img, code_dict) 
    decode_dict = data_processing.flip_dictionary(code_dict)    
    decode_dict = data_processing.dictionary_to_binary(decode_dict) 
    header = np.zeros(200)
    args = [header, dimensions, encoded_img, header, decode_dict, header]
    data= np.concatenate(args)
    data = data_processing.expand(data)
    data = data_processing.complexize_data(data)
    write_to_file(data)

def write_to_file(complex_array):
    """ Takes in np array with complex values & writes them to file """
    # source; https://stackoverflow.com/questions/29809988/numpy-array-tofile-binary-file-looks-strange-in-notepad
    filename = "fileOutput.dat"
    fileobj = open(filename, mode='wb')
    off = np.array(complex_array, dtype=np.float32)
    off.tofile(fileobj)
    fileobj.close()

    
if __name__ == '__main__':
    img = cv2.imread('dog.jpg')

    # EXAMPLE TEST OF USE
    #test_img = np.array([[1, 2, 5, 6, 2], [2, 5, 3, 5, 1], [3, 6, 1, 5, 1]])
    #main(test_img)
   
    #a = np.array([0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1])
    a = np.array([0, 0, 0, 1, 1, 0] * 10000)
    print len(a)
    a = data_processing.expand(a)
    a = data_processing.complexize_data(a)
    write_to_file(a)
