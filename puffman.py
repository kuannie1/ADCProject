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
	print res
	return res

if __name__ == '__main__':

	puffman({'010':5, '011': 7, '1':2}, np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]))
	# expect to return [2 5 7 5 2] 