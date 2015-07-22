#Tree and associated methods
#dummy = 0, noisy = -1, real = 1

import math

class Tree:
    
    def __init__(self, nodeNumber, z): #creates the tree
        
        assert (nodeNumber % 2 == 1), "tree must have odd number of buckets"
        
        self._buckets = [[0 for i in range(z)] for i in range(nodeNumber)]
        
        self._z = z
        self._size = nodeNumber
        self._height = int(math.log(self._size+1,2))
        self._numAccesses = 0
    
    def RLOLeaf(self): #returns next Reverse Lexicographic Leaf

        binary = (bin(self._numAccesses)[2:]).zfill(self._height - 1) 
        #print (str(binary))

 
        binary = binary[::-1]
        self._numAccesses += 1
        self._numAccesses = (self._numAccesses)%(int(math.pow(2,self._height - 1)))
        resp = self._size -(int(binary,2))
        #print ("will return %d" %resp)
        return resp
    
    def getPathNodes(leaf): #returns all buckets along the path to a specified leaf
        
        result = []
        
        while (leaf > 0):
            result.insert(0 , leaf)
            leaf = leaf >> 1
            
        return result
