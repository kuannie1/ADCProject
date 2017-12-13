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
	counter = 0
	for val in img:
		
		curr += str(int(val))
		if curr in decode_dict:
			res.append(decode_dict[curr])
			curr = ''
	return res

def to_array(img, dimensions):
	""" Converts 1d img array into 2d array according to dimensions """

	if len(dimensions) != 32:
		print('Error: dimensions should be 32 bits long,', 
			'containing a 16 bit number for h and a 16 bit number for w')
	# Retreive h and w dimensions from bits in array 
	h = ''
	w = ''
	for i in range(16):
		h += str(int(dimensions[i]))
		w += str(int(dimensions[i+16]))

	h = int(h,2)
	w = int(w,2)
	print('h in puffman to_array=', h)
	print('w in puffman to_array=', w)
	res = np.zeros((h,w))

	for row_index in range(0, h):
		for col_index in range(0, w):
			res[row_index][col_index] = img[col_index + row_index * w]

	return res
			
if __name__ == '__main__':
	pass
	