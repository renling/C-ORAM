import math
import random

#Tree and associated methods
#zero = 0, noisy = -1, real = 1

class TreeNode:

	def __init__(self):
		self._left=None
		self._right=None
		self._data = []
		self._metadata=[] #corresponds to _data, tells each piece of data where to go

	def getLeft(self, node):
		return node._left;

	def getRight(self, node):
		return node._right;


	def pushdown(self): #pushes contents to children
		