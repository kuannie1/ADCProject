# Given dictionary of characters and frequencies

#Example
# freq_dict = {'A': .7, 'B': .03, 'C': .07, 'D': .01, 'E': .06, 'F': .04, 'G': .089, 'H': .001}

class tree:
	""" the tree class for process of huffman coding"""
	def __init__(self, value=None, frequency=0, left_child=None, right_child=None):
		self.frequency = frequency
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


def make_huffman_tree(freq_dict):
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
