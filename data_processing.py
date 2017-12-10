"""
Data processing used for USRP wireless communication.
"""
import numpy as np
import cv2
import huffman


def flip_dictionary(code_dict):
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	return reversed_code_dict


def dictionary_to_binary(input_dict):
	""" Converts the dictionary to np array of bits
	where every 8 bits alternatingly represent keys and values.
	Assumes keys and values are numbers. """

	res = []
	for k, v in input_dict.iteritems():
		res += make_binary_list(k)
		res += make_binary_list(v)

	return np.array(res)

def binary_to_dictionary(binary_dict_array):
	# takes in np array of bits where every 8 bits alternatingly represent
	# keys and values in a dictionary.
	res = {}

	for i in range(0, len(binary_dict_array), 16):
		key = ''
		val = ''
		for j in range(8):
			key += str(binary_dict_array[i + j])
			val += str(binary_dict_array[i + j + 8])

		res[int(key, 2)] = int(val,2)

	return res

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



def complexize_data(nparray_data):
    """ Takes in results from data_to_write and makes every other index complex """
    print nparray_data
    list_data = list(nparray_data)
    for i in range(1, len(list_data), 2):
        list_data[i] = 1j*list_data[i]
    result = np.array(list_data)
    print result


if __name__ == '__main__':
    b =  dictionary_to_binary({5:2, 1:7, 8:12})
    print binary_to_dictionary(b)
    print b