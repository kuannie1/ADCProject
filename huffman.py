# Given dictionary of characters and frequencies

#Example
#freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}

class tree:
	""" the tree class for process of huffman coding"""
	def __init__(self, value=None, frequency=0, left_child=None, right_child=None):
		self.frequency = frequency
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


def make_huffman_tree(freq_dict):
	""" generates tree for huffman coding """
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

def code_from_tree(huff_tree, code = '', code_dict=dict()):
	""" generates dictionary of encoding from tree """

	if huff_tree.value:
		code_dict[huff_tree.value] = code
		

	if huff_tree.left_child:
		code_dict.update(code_from_tree(huff_tree.left_child, code= code + '0', code_dict = code_dict))

	if huff_tree.right_child:
		code_dict.update(code_from_tree(huff_tree.right_child, code= code + '1', code_dict= code_dict))

	return code_dict




def test_example_code_from_tree():
	""" checks values of generated code from tree made from example frequency dictionary """
	freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}
	huff_tree = make_huffman_tree(freq_dict)
	code_dict = code_from_tree(huff_tree)
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	print code_dict

	assert huff_tree.right_child.value == reversed_code_dict['1']
	assert huff_tree.left_child.left_child.left_child.value == reversed_code_dict['000']	
	assert huff_tree.left_child.right_child.right_child.value == reversed_code_dict['011']

def encode_string(input_string, code_dict):
	res = ''
	for char in input_string:
		res += code_dict[char]
	return res

def dictionary_to_binary(code_dict):
	binary_dictionary = ''
	dict_string = str(code_dict)
	for char in dict_string:
		binary_dictionary += bin(ord(char))[2:]
	
	return binary_dictionary

