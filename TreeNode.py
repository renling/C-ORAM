import math
import random
import Tree
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
		#eviction

	def merge(self, bucket1, bucket2): #aligns buckets pseudo-randomly for merging and merges them #copied from tree
        
        #Assumes that both buckets are pseudo-random
        
        zeroes1 = []
        noisys1 = []
        zCount1 = 0
        nCount1 = 0
        rCount2 = 0
        nCount2 = 0
        
        for i in range(len(bucket1)): #gathers metadata
            
            if(bucket1[i] == 0):
                zeroes1.append(i)
                zCount1 += 1
                
            if(bucket1[i] == -1):
                noisys1.append(i)
                nCount1 += 1
                
            if(bucket2[i] == 1):
                rCount2 += 1
            
            if(bucket2[i] == -1):
                nCount2 += 1
        
        assert ((rCount2 + nCount2 <= nCount1 + zCount1) and (rCount2 < zCount1)), "BUCKET OVERFLOW ERROR"        
                
        #assign reals spaces among zeroes
        #assign noisys spaces among noisys (and zeroes if insufficient space)
        
        r2map = self.AssignFromList(rCount2, zeroes1) #this and below 2 lines handle output from assignment function
        zeroes1 = r2map[1] #now only the empty locations
        r2map = r2map[0]
        
        if nCount2 > nCount1:
            ndiff = nCount2 - nCount1
            
            n2map = noisys1
            n2map += self.AssignFromList(ndiff, zeroes1)[0]
            
        else:
            n2map = self.AssignFromList(nCount2, noisys1)[0]
        
        
        #below lines are for testing only, obviously need to be fixed for real data   
        for i in range(len(r2map)): #assign reals
            bucket1[r2map[i]] = 1
        for i in range(len(n2map)):
            bucket1[n2map[i]] = -1
            
        return bucket1