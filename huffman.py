# Given dictionary of characters and frequencies

#Example
#freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}

import numpy as np
import cv2
import frequency_calculator
import data_processing

class tree:
	""" the tree class for process of huffman coding"""
	def __init__(self, value=None, frequency=0,
		left_child=None, right_child=None):
		self.frequency = frequency
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


def make_huffman_tree(freq_dict):
	""" Generates tree for huffman coding. """

	sub_trees = []

	# initialize with each character as its own tree/node
	for k,v in freq_dict.iteritems():
		sub_trees.append(tree(value=k, frequency=v))

	while len(sub_trees) > 1:
		# sort by frequency
		sub_trees.sort(key = lambda x: x.frequency)
		# make new subtree from two smallest trees
		new_tree = tree(
			frequency = sub_trees[0].frequency + sub_trees[1].frequency,
			left_child = sub_trees[0],
			right_child = sub_trees[1])
		sub_trees = [new_tree] + sub_trees[2:]

	# pop single tree from list
	huffman_tree = sub_trees.pop(0)
	return huffman_tree

def code_from_tree(huff_tree, code = '', code_dict=dict(), top=True):
	""" Generates dictionary of encoding from tree. """

	if huff_tree.value:
		code_dict[huff_tree.value] = code
		

	if huff_tree.left_child:
		code_dict.update(code_from_tree(huff_tree.left_child,
			code= code + '0', code_dict = code_dict, top = False))

	if huff_tree.right_child:
		code_dict.update(code_from_tree(huff_tree.right_child,
			code= code + '1', code_dict= code_dict, top = False))

	return code_dict


def encode_image(img, code_dict):
	""" given an image, converts each numerical value in the 
	image matrix to 0's and 1's using huffman encoding """
	# assume img is a w by h 2D 
	# h = num rows
	# w = num cols
	(h, w) = img.shape
	res = []
	# loop through each pixel in res
	# and assign encoded value
	for row_index in range(0, h):
		for col_index in range(0, w):

			binary_string = code_dict[float(img[row_index][col_index])]
			binary_list = [int(d) for d in binary_string]
			res += binary_list
	print('h=',h)
	h = data_processing.make_binary_list(h, eight_bit =False, sixteen_bit=True)
	w = data_processing.make_binary_list(w, eight_bit =False, sixteen_bit=True)
	print('h=',h)
	print('w=', w)
	dimensions = np.array(h + w)
	print('dimensions=', dimensions)
	res = np.array(res)
	# returns res = np array of numbers and dimesnions = np array of numbers
	return (res, dimensions)


 


if __name__ == '__main__':
	pass