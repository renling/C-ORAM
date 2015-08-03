import math
import random

class TreeNode:

	def __init__(self):
		self._left=None
		self._right=None
		self._data = []

	def getLeft(self, node):
		return node._left;

	def getRight(self, node):
		return node._right;


	def pushdown(self): #pushes contents to children
		