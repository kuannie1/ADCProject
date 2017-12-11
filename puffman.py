# Given transmitted dictionary and encoded message, return original message.

import numpy as np

def puffman(img, decode_dict):
	"""Given dictionary of huffman encoding and
	message representing image, decode back to
	original numeric values of image array"""

	# image as encoded 1-D array before transformed
	# not including dimensions

	# code dict has bit strings as keys and integers as values

	res = []
	curr = ''
	for val in img:
		curr += str(val)
		if curr in decode_dict:
			res.append(decode_dict[curr])
			curr = ''
	return res

def to_array(img, dimensions):
	""" Converts 1d img array into 2d array according to dimensions """

	# NEEDS TEST

	if len(dimensions) != 16:
		print('Error: dimensions should be 16 bits long,', 
			'containing an 8 bit number for h and an 8 bit number for w')
	# Retreive h and w dimensions from bits in array 
	h = ''
	w = ''
	for i in range(8):
		h += str(dimensions[i])
		w += str(dimensions[i+8])

	h = int(h,2)
	w = int(w,2)

	res = np.zeros((h,w))

	for row_index in range(0, h):
		for col_index in range(0, w):
			res[row_index][col_index] = img[col_index + row_index * w]

	return res
			
if __name__ == '__main__':

	p = puffman(np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1]), {'010':5, '011': 7, '1':2},)
	print p
	# expect puffman to return [2 5 7 5 2 2] 
	a = to_array(p, np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0]))
	print a
	# expect to return [[2 5] [7 5] [2 2] 
	