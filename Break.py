from Tree import Tree
import math
import random


def ForceDupPerm(attack):
	ORAMsize = (1 << 3) - 1
	Z = 40
	A = 20
	tree = Tree(ORAMsize, Z)

	DummyRoot = [0] * A
	
	# eviction 1
	root = [tree.randomLeaf() for i in range(A)] 
	if attack == False:
		root = DummyRoot       
	ret = tree.evictAll(root)
	Pi1, parent1, child1 = ret[0][0], ret[0][1], ret[0][2]

	# eviction 2
	root = [tree.randomLeaf() for i in range(A)]        
	if attack == False:
		root = DummyRoot       
	ret = tree.evictAll(root)
	Pi2, parent2, child2 = ret[0][0], ret[0][1], ret[0][2]

	# eviction 3
	root = DummyRoot  	# keep doing dummy accesses for this epoch        
	ret = tree.evictAll(root)
	Pi3, parent3, child3 = ret[1][0], ret[1][1], ret[1][2]

	# these two perm should look similar
	#child2p = [0] * Z
	#for j in range(Z):
	#	child2p[Pi1[j]] = child2[j]
	#print(Pi1, parent1, child1)
	#print(Pi2, parent2, child2)
	#print(Pi3, parent3, child3)
	#print('\n')

	# count the number of repetition
	dup = 0
	for j in range(Z):
		dup += (Pi3[j] == Pi1[Pi2[j]])
	return dup	

def breakCORAM():
	numTest = 1000
	dup1 = 0
	for k in range(numTest):
		dup1 += ForceDupPerm(True)

	dup2 = 0
	for k in range(numTest):
		dup2 += ForceDupPerm(False)

	print(dup1, dup2)

	
breakCORAM()	
