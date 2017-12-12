"""
Tests used in development. Import files as needed.
"""
import numpy as np
import cv2
import huffman	
import data_processing

def test_complexize_decomplexize():
	a = np.random.rand(10)
	c = data_processing.complexize_data(a)
	for i in range(0, 20, 2):
		assert c[i+1] == np.imag(c[i])
		assert c[i] == a[i/2]
	d = data_processing.decomplexize_data(c)
	assert  a.all() == d.all()
	
def test_example_code_from_tree():
	freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}
	huff_tree = huffman.make_huffman_tree(freq_dict)
	code_dict = huffman.code_from_tree(huff_tree)
	reversed_code_dict = data_processing.flip_dictionary(code_dict)
	assert huff_tree.right_child.value == reversed_code_dict['1']
	assert huff_tree.left_child.left_child.left_child.value == reversed_code_dict['000']	
	assert huff_tree.left_child.right_child.right_child.value == reversed_code_dict['011']


if __name__ == '__main__':
	test_complexize_decomplexize()
	test_example_code_from_tree