"""
Tests used in development. Import files as needed.
"""

import huffman	

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
