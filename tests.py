"""
Tests used in development. Import files as needed.
"""
import numpy as np
import cv2
import huffman	
import data_processing
import puffman

def puffman_to_array():
	p = puffman.puffman(np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1]), {'010':5, '011': 7, '1':2},)
	assert p == [2, 5, 7, 5, 2, 2]

	a = puffman.to_array(p, np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0]))
	assert np.array_equal(np.array([[2, 5], [7, 5], [2,2]]),a)

def test_data_from_array():
	h = np.zeros(20)
	h[9] = 1
	dim = np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0])
	im = np.array([1,1,1,1,1,1,0,0,1,0])
	dct = np.array([1,0,1,0,1,0,1,0,1,0,1])
	args = [h, dim, im, h, dct, h, h]
	data = np.concatenate(args)
	[dimensions, image, decode_dict] = data_processing.data_from_array(data, h)
	assert np.array_equal(dim, dimensions)
	assert np.array_equal(im, image)
	assert np.array_equal(dct, decode_dict)

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
	test_example_code_from_tree()
	puffman_to_array()
	test_data_from_array()