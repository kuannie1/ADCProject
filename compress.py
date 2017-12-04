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
from frequency_calculator import get_frequencies

if __name__ == '__main__':
    pass
