#Tree and associated methods
#dummy = 0, noisy = -1, real = leafID

import time
import math
import random
from copy import deepcopy

class Tree:
    
    seed = 0 #for block contents
    
    def __init__(self, nodeNumber, z): #creates the tree        
        assert (nodeNumber % 2 == 1), "tree must have odd number of buckets"        
        self._buckets = [ [0] * z for i in range(nodeNumber)]	# [[0]*z]*nodeNumber will cause problems, why?
        
        self._z = z
        self._size = nodeNumber
        self._height = int(math.log(self._size+1, 2))
        self._numAccesses = 0
        self._attack = True    
    
    def RLOLeaf(self): #returns next Reverse Lexicographic Leaf
        binary = (bin(self._numAccesses)[2:]).zfill(self._height - 1)        
        binary = binary[::-1]
        self._numAccesses += 1
        resp = self._size / 2 + 1 + (int(binary, 2))
        #print ("RLO leaf =  %d" %resp, binary)
        return resp
    
    def randomLeaf(self):
        return random.randint(int(self._size / 2) + 1, self._size)
    
    def getPathNodes(self, leaf): #returns all buckets along the path to a specified leaf        
        result = []       
        while (leaf > 0):
            result.insert(0 , leaf)
            leaf = leaf >> 1            
        return result
    
    def getBucket(self, bucketID): #subtracts 1 because arrays go up from 0
        return self._buckets[bucketID-1]
    
    def clearBucket(self, bucketID):
        self._buckets[bucketID-1] = [0] * self._z
        
    def setBucket(self, bucketID, contents):
        self._buckets[bucketID-1] = deepcopy(contents)

    def copyBucket(self, dst, src):
        self._buckets[dst-1] = deepcopy(self._buckets[src-1])
        
    def merge(self, child, parent):
        parentBucket = self.getBucket(parent)
        childBucket = self.getBucket(child)
        childOld = deepcopy(childBucket)
        for block in parentBucket: # insert real and noisy
            if (block == 0): #noisy or real
                continue
            if block == -1:
                block = -2	# tmp use of -2 to mark used noisy			
            if block == -2 and -1 in childBucket: # noisy aligns with noisy first			
                childBucket[childBucket.index(-1)] = -2    
            else:
                if 0 not in childBucket:
                    print("Bucket overflows at level " + str(self._level))
                    print(parent, child, self.getBucket(parent), self.getBucket(parent)) 
                childBucket[childBucket.index(0)] = block
        for i in range(len(childBucket)): # insert real and noisy
            if childBucket[i] == -2:
                childBucket[i] = -1		
		        
        if not self._attack:
            return
 
        # If trying to attack, return the public permutation sent to the server
        # Below is more detailed simulation                
        parentRealSet = set([i for i in range(self._z) if parentBucket[i] > 0])
        parentZeroSet = set([i for i in range(self._z) if parentBucket[i] == 0])
        parentNoiseSet = set([i for i in range(self._z) if parentBucket[i] < 0])
        childRealSet = set([i for i in range(self._z) if childOld[i] > 0])
        childZeroSet = set([i for i in range(self._z) if childOld[i] == 0])
        childNoiseSet = set([i for i in range(self._z) if childOld[i] < 0])

        #print("the 3 sets: ", childRealSet, childZeroSet, childNoiseSet)
        r1 = len(parentRealSet)
        dstRealList = random.sample(childZeroSet, r1)
        childZeroSet -= set(dstRealList)
        
        n1 = len(parentNoiseSet)
        n2 = len(childNoiseSet)
        if n1 <= n2:
            dstNoiseList = random.sample(childNoiseSet, n1)
            childNoiseSet -= set(dstNoiseList)
        else:
            dstNoiseList = list(childNoiseSet) + random.sample(childZeroSet, n1-n2)
            random.shuffle(dstNoiseList)
            childZeroSet -= set(dstNoiseList)
            childNoiseSet -= set(dstNoiseList)

        z1 = len(parentZeroSet)
        dstZeroSet = childRealSet | childZeroSet | childNoiseSet
        assert(z1 == len(dstZeroSet)), "Something is wrong in merging ... "
        dstZeroList = random.sample(dstZeroSet, z1)

        Pi = [0] * self._z
        for src, dst in zip(parentRealSet, dstRealList):
            Pi[src] = dst
            childBucket[dst] = parentBucket[src]
        for src, dst in zip(parentNoiseSet, dstNoiseList):
            Pi[src] = dst
            childBucket[dst] = parentBucket[src]
        for src, dst in zip(parentZeroSet, dstZeroList):
            Pi[src] = dst
            childBucket[dst] = childOld[dst] # + 0

        #print(parent, child, parentBucket, childOld, childBucket, Pi)        
        return [Pi, parentBucket, childOld]
                   
    def evictToKids(self, parent, child, sibling):                
        # copy parent to sibling
        self.copyBucket(sibling, parent)		
        self.makeNoisy(sibling, sibling)
		
        Pi = [ [0]*self._z ] * 3
        if self._numAccesses == 1 and False:	# for ease of the attack, no need to permute if child is known to be empty
            self.copyBucket(child, parent)		
            self.makeNoisy(child, child)
        else:	
			# merge parent and child, after marking noise properly in parent
            self.makeNoisy(parent, child)		
            Pi = self.merge(child, parent)			
        return Pi        
					    
    def makeNoisy(self, src, target):
        bucket = self.getBucket(src)	    
        for i in range(len(bucket)):
            if bucket[i] >= 1 and (target not in self.getPathNodes(bucket[i])):      # check if path contains bucketID       
                bucket[i] = -1 # now it's noisy!					
        
    def evictAll(self, input):	
        input = input + [0 for i in range(self._z - len(input))]
        random.shuffle(input)
        self.setBucket(1, input)
        
        rlo = self.RLOLeaf()       
        
        PI = []     	
        self._level	= 0;	
        path = self.getPathNodes(rlo)        
        for self._level in range(len(path)-1):
            parent = path[self._level]
            child = path[self._level+1]
            sibling = child + 1 - 2 * (child % 2)
            PI += [self.evictToKids(parent, child, sibling)]            	
        self.cleanBucket(rlo)         # clean up leaf
        return PI
    
    def cleanBucket(self, bucketID):
        for i in range(self._z):
            if self._buckets[bucketID - 1][i] == -1:
                self._buckets[bucketID - 1][i] = 0
                #break #only clean one
    
    def readBlock(self, leaf):
        for bucketID in reversed(self.getPathNodes(leaf)):
            if leaf in self._buckets[bucketID-1]:
                self._buckets[bucketID-1].index(leaf) == 0
                return 1				
        return 0				
        
        
        
        
        
