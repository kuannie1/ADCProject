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
import numpy as np
from scipy import stats

def unexpand_and_correct(arr, expand_scale = 50):
	""" Given a received 1-D np array (expanded before transimission), 
	retrieve original 0s and 1s array from before expansion
	correcting for errors in process """

	res = []

	# convert to 0s and 1s.
	for i in range(len(arr)):
		if arr[i] > 0:
			arr[i] = 1
		else:
			arr[i] = 0
	res_length = int(math.ceil(len(arr)/expand_scale))
	for i in range(res_length):
		if (i+1)*expand_scale  < len(arr):		
			# arr[0: 50], arr[50:100], arr[100: 150]
			val = stats.mode(arr[i*expand_scale: (i+1)*expand_scale])[0]
		else:
			val = stats.mode(arr[i*expand_scale:])[0]
		res.append(val[0])
	
	return np.array(res)

def read_from_file(filename):
	fileobj2 = open(filename, mode='rb')
	off = np.fromfile(fileobj2, dtype = np.float32)
	print(off)
	fileobj2.close()

if __name__ == '__main__':
   print unexpand_and_correct(np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1]), 5)
