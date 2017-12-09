# Given dictionary of characters and frequencies

#Example
#freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}

import numpy as np
import cv2
import frequency_calculator

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

	if top:
		for k in code_dict:
			code_dict[k] = int(code_dict[k],2)
	
	# returns dictionary of {val number: code number}
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
			decimal_val = code_dict[img[row_index][col_index]]
			binary_val = bin(decimal_val)[2:]
			binary_list = [int(d) for d in binary_val]
			res += binary_list
	
	h = make_binary_list(h)
	w = make_binary_list(w)

	dimensions = np.array(h + w)
	res = np.array(res)
	# returns res = np array of numbers and dimesnions = np array of numbers
	return (res, dimensions)


def flip_dictionary(code_dict):
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	return reversed_code_dict


def dictionary_to_binary(input_dict):
	""" Converts the dictionary to binary.
	Assumes keys and values are numbers. """

	res = []
	res += make_binary_list(ord('{'))
	for k, v in input_dict.iteritems():
		res += make_binary_list(k)
		res += make_binary_list(ord(':'))
		res += make_binary_list(v)
	res += make_binary_list(ord('}'))

	return np.array(res)

def expand(input_array):
	""" Given a binary input array, change 0 values to -1 
	and expand such that each value in the array is
	repeated 50 times. """

	
	expanded = []
	for val in input_array:
		if val == 0:
			val = -1
		elif val == 1:
			val = int(val)
		else:
			print("non-binary input to expand")
		print val
		for i in range(0,50):
			expanded.append(val)

	expanded_array = np.array(expanded)
	return expanded_array

def make_binary_list(num, eight_bit=True):
	""" Takes in decimal number, converts to binary and returns list of bits"""
	if eight_bit:
		num = format(num,'08b')
	else:
		num = bin(num)[2:]

	return [int(d) for d in num]

def data_to_write(img, huff_tree):
	""" Creates final np array of -1s and 1s to be written to file"""

 	code_dict = code_from_tree(huff_tree) # dictionary {number: number}
 	encoded_img, dimensions = encode_image(img, code_dict) #[numbers], [number number]
 	decode_dict = flip_dictionary(code_dict)  	# dictionary {number:nnumber}
 	decode_dict = dictionary_to_binary(decode_dict) 
 	header = np.zeros(200)
	args = [header, dimensions, encoded_img, header, decode_dict, header]
 	data= np.concatenate(args)
 	data = expand(data)
 	return data

def complexize_data(nparray_data):
	""" Takes in results from data_to_write and makes every other index complex """
 	print nparray_data
 	list_data = list(nparray_data)
 	for i in range(1, len(list_data), 2):
 		list_data[i] = 1j*list_data[i]
 	result = np.array(list_data)
 	print result

def write_to_file(complex_array):
	""" Takes in np array with complex values & writes them to file """
	# source; https://stackoverflow.com/questions/29809988/numpy-array-tofile-binary-file-looks-strange-in-notepad
	filename = "fileOutput.dat"
	fileobj = open(filename, mode='wb')
	off = np.array(complex_array, dtype=np.float32)
	off.tofile(fileobj)
	fileobj.close()

	fileobj2 = open(filename, mode='rb')
	off = np.fromfile(fileobj2, dtype = np.float32)
	print(off)
	fileobj2.close()

 	

def test_example_code_from_tree():
	""" Checks values of generated code from tree made from example frequency dictionary """

	# JUST A TEST
	freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}
	huff_tree = make_huffman_tree(freq_dict)
	code_dict = code_from_tree(huff_tree)
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	print code_dict

	assert huff_tree.right_child.value == reversed_code_dict['1']
	assert huff_tree.left_child.left_child.left_child.value == reversed_code_dict['000']	
	assert huff_tree.left_child.right_child.right_child.value == reversed_code_dict['011']



if __name__ == '__main__':
 	img = cv2.imread('dog.jpg')
 	arr = np.array([0,1])

 	# EXAMPLE TEST OF USE
 	test_img = np.array([[1, 1, 5, 6, 2], [2, 1, 3, 5, 1], [3, 1, 1, 5, 1]])
 	freqs = frequency_calculator.get_frequencies(test_img)
 	huff_tree = make_huffman_tree(freqs)
 	code_dict = code_from_tree(huff_tree)
 	encoded_img, dimensions = encode_image(test_img, code_dict)

 	dataToWrite = data_to_write(test_img, huff_tree)
 	complexizedData = complexize_data(dataToWrite)
 	write_to_file(complexizedData)
 	# based on data to write, get 


