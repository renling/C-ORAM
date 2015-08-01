#Tree and associated methods
#dummy = 0, noisy = -1, real = 1

import math
import random

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
    
    def getPathNodes(self, leaf): #returns all buckets along the path to a specified leaf
        
        result = []
        
        while (leaf > 0):
            result.insert(0 , leaf)
            leaf = leaf >> 1
            
        return result
    
    def getBucket(self, bucketID): #subtracts 1 because arrays go up from 0
        return self._buckets[bucketID - 1]
    
    def merge(self, bucket1, bucket2): #aligns buckets pseudo-randomly for merging and merges them
        
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
        
           
    def insertData(self, data):
        
    
            
    def AssignFromList(self, objnum, locs): #randomly assigns objects locations from specified list
        
        assert(objnum <= len(locs)), "Pigeon-hole Principle Violation"
        
        mapping = []
        
        for i in range(objnum):
            
            newloc = locs[random.randint(0,len(locs) - 1)]
            mapping.append(newloc)
            locs.remove(newloc)
        
        
        return [mapping, locs]
    
        
        
        
