#Tree and associated methods
#dummy = 0, noisy = -1, real = leafID

import time
import math
import random

class Tree:
    
    seed = 0 #for block contents
    
    def __init__(self, nodeNumber, z): #creates the tree
        
        assert (nodeNumber % 2 == 1), "tree must have odd number of buckets"
        
        self._buckets = [[0 for i in range(z)] for i in range(nodeNumber)]
        
        self._z = z
        self._size = nodeNumber
        self._height = int(math.log(self._size+1,2))
        self._numAccesses = 0
        
        self._leaves = [i for i in range(2 ** (self._height - 1), 2 ** self._height)] 
            #leaf locations
    
    def RLOLeaf(self): #returns next Reverse Lexicographic Leaf
        binary = (bin(self._numAccesses)[2:]).zfill(self._height - 1) 
        #print (str(binary))
 
        binary = binary[::-1]
        self._numAccesses += 1
        self._numAccesses = (self._numAccesses)%(int(math.pow(2,self._height - 1)))
        resp = self._size -(int(binary,2))
        #print ("RLO leaf =  %d" %resp)
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
        return self._buckets[bucketID - 1]
    
    def clearBucket(self, bucketID):
        self._buckets[bucketID - 1] = [0 for i in range(self._z)]
        
    def setBucket(self, bucketID, contents):
        self._buckets[bucketID - 1] = contents

    def copyBucket(self, dst, src):
        self._buckets[dst - 1] = [self._buckets[src - 1][i] for i in range(self._z)]
		
    def merge(self, child, parent):
        parentBucket = self.getBucket(parent)
        childBucket = self.getBucket(child)		
        for block in parentBucket: # insert real and noisy
            if (block == 0): #noisy or real
                continue
            if block == -1:
                block = -2	# tmp use of -2 to mark used noisy			
            if block == -2 and -1 in childBucket: # noisy aligns with noisy first			
                childBucket[childBucket.index(-1)] = -2    
            else:
                if (0 not in childBucket):
                    print("BUCKET OVERFLOW ERROR at level " + str(self._level)) 
                childBucket[childBucket.index(0)] = block
        for i in range(len(childBucket)): # insert real and noisy
            if childBucket[i] == -2:
                childBucket[i] = -1				
        return
 
        # Below is more detailed simulation; assumes that both buckets are pseudo-random
		
        zeroes1 = []
        noisys1 = []
        real2 = []
		
        zCount1 = bucket1.count(0)
        nCount1 = bucket1.count(-1)
        nCount2 = bucket2.count(-1)
        rCount2 = 0		
		
        for i in range(len(bucket1)): #gathers metadata
            
            if(bucket1[i] == 0): #dummy
                zeroes1.append(i)
                
            if(bucket1[i] == -1): #noisy
                noisys1.append(i)
                
            if(bucket2[i] >= 1): #real
                real2.append(bucket2[i])
                rCount2 += 1
                    		
        assert ((rCount2 + nCount2 <= nCount1 + zCount1) and (rCount2 <= zCount1)), "BUCKET OVERFLOW ERROR"        
        					
        #assign reals spaces among zeroes
        #assign noisys spaces among noisys (and zeroes if insufficient space)
                			
        r2map = self.AssignFromList(rCount2, zeroes1) #this and below 2 lines handle output from assignment function
        #print('r2map is' + str(r2map))
        zeroes1 = r2map[1] #now only the empty locations
        r2map = r2map[0]
        
        if nCount2 > nCount1:
            ndiff = nCount2 - nCount1
            
            n2map = noisys1
            n2map += self.AssignFromList(ndiff, zeroes1)[0]
            
        else:
            n2map = self.AssignFromList(nCount2, noisys1)[0]
        	
        for i in range(len(r2map)): #assign reals
            bucket1[r2map[i]] = real2[i]
        for i in range(len(n2map)):
            bucket1[n2map[i]] = -1
        
        #print('Merged: ' + str(bucket1))            
        return bucket1
                   
    def AssignFromList(self, objnum, locs): #randomly assigns objects locations from specified list
        
        assert(objnum <= len(locs)), "Pigeon-hole Principle Violation"
        
        #print(str(locs) + ',  ' + str(objnum))
        
        
        rands = random.sample(range(0, len(locs)), objnum)
        #print( 'rands are ' + str(rands))
        mapping = []
        
        for i in range(len(rands)):            
            mapping.append(locs[rands[i]])
        
        for i in range(len(mapping)):
            locs.remove(mapping[i])
            
        #print(locs)
        #print('mapping is ' + str(mapping))
        
        return [mapping, locs]
   
    def evictToKids(self, parent, child, sibling):        
        #print(self.getBucket(parent))
        #print(self.getBucket(child))		
        #print(self.getBucket(sibling))
		
        # copy parent to sibling
        self.copyBucket(sibling, parent)		
        self.makeNoisy(sibling, sibling)
		
		# merge parent and child, after marking noise properly in parent
        self.makeNoisy(parent, child)		
        self.merge(child, parent)			
        					
        #print(self.getBucket(parent))
        #print(self.getBucket(child))		
        #print(self.getBucket(sibling))
        return
    
    def makeNoisy(self, src, target):
        bucket = self.getBucket(src)	    
        for i in range(len(bucket)):
            if bucket[i] >= 1 and (target not in self.getPathNodes(bucket[i])):      #check if path contains bucketID       
                    bucket[i] = -1 #now it's noisy!					
        
    def evictAll(self, input):	
        input = input + [0 for i in range(self._z - len(input))]
        self.setBucket(1, input)
        
        rlo = self.RLOLeaf()       
             	
        self._level	= 0;	
        path = self.getPathNodes(rlo)
        for self._level in range(len(path)-1):
            parent = path[self._level]
            child = path[self._level+1]
            sibling = child + 1 - 2 * (child % 2)
            self.evictToKids(parent, child, sibling)
         		
        self.cleanBucket(rlo)         #clean up leaf
        return
    
    def cleanBucket(self, bucketID):
        for i in range(self._z):
            if self._buckets[bucketID - 1][i] == -1:
                self._buckets[bucketID - 1][i] = 0
                break #only clean one
    
    def readBlock(self, leaf):
        for bucketID in reversed(self.getPathNodes(leaf)):
            if leaf in self._buckets[bucketID-1]:
                self._buckets[bucketID-1].index(leaf) == 0
                return 1				
        return 0				
        
        
        
        
        
