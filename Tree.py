#Tree and associated methods
#dummy = 0, noisy = -1, real = 1

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
        #print ("will return %d" %resp)
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
        return
        
    def setBucket(self, bucketID, contents):
        self._buckets[bucketID - 1] = contents
        self._buckets[bucketID - 1] += [0 for i in range(self._z - len(self._buckets[bucketID - 1]))]
        return
    
    def merge(self, bucket1, bucket2): #aligns buckets pseudo-randomly for merging and merges them
        #print('B1: ' + str(bucket1))
        #print('B2: ' + str(bucket2))
        #Assumes that both buckets are pseudo-random
        
        for block2 in bucket2: # insert real and noisy
            if (block2 != 0): #noisy or real
                if block2 == -1 and -1 in bucket1: # noisy aligns with noisy first			
                    bucket1[bucket1.index(-1)] = -1    
                else:
                    assert (0 in bucket1), "BUCKET OVERFLOW ERROR"  
                    bucket1[bucket1.index(0)] = block2  	
   								
        return bucket1
				
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

         
    # def eviction(self,input): #initial
    #     self.setBucket(1, input)
    #     nextLeaf = RLOLeaf()
    #     leaves=getPathNodes(nextLeaf)
    #     for i in range(len(leaves)):

    #         curBucket=leaves[i]
    #         getBucket(2*(i+1))=merge(leaves[i],getBucket(2*(i+1)))
    #         getBucket(2*(i+1)+1=merge(leaves[i],getBucket(2*(i+1)+1))

    #         for j in range(len(curBucket)):
    #             curBucket[j]=0

    #     return


            
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
    
    def levelNumber(self, bucket):#returns the level a leaf is on (used in getMaxLevel)
        #print bucket
        a = int(math.log(bucket,2))

        return a
    
    def children(self, bucketID): 
        assert(self.levelNumber(bucketID) < self._height - 1), "Leaves have no children"
        
        return [2 * bucketID, 2 * bucketID + 1] #IDs of children
    
    def evictToKids(self, bucketID):
        
        kids = self.children(bucketID)
        
        kidContents = [self.merge(self.getBucket(kids[0]),self.getBucket(bucketID)), 
                self.merge(self.getBucket(kids[1]),self.getBucket(bucketID))]
        					
        self.clearBucket(bucketID)
		
        kidContents[0] = self.makeNoisy(kidContents[0], kids[0])
        kidContents[1] = self.makeNoisy(kidContents[1], kids[1])      
        #print(kidContents)
		
        self.setBucket(kids[0], kidContents[0])
        self.setBucket(kids[1], kidContents[1])
        
        return
    

    def makeNoisy(self, bucket, bucketID):
        for i in range(len(bucket)):
            if bucket[i] >= 1:
                path = self.getPathNodes(bucket[i]) + [bucket[i]]
                #check if bucket path + leaf contains bucketID
                if not ((bucketID) in path):
                    bucket[i] = -1 #now it's noisy!
        
        return bucket
        
    def evictAll(self, input):	
        input = input + [0 for i in range(self._z - len(input))]
        self.setBucket(1, input)
        
        rlo = self.RLOLeaf()       
             		
        for node in self.getPathNodes(rlo):
            self.evictToKids(node)
         		
        self.cleanBucket(rlo)
        #clean up leaf
        return
    
    def cleanBucket(self, bucketID):
        for i in range(self._z):
            if self._buckets[bucketID - 1][i] == -1:
                self._buckets[bucketID - 1][i] = 0
                #break #only clean one
    
    def readBlock(self, leaf):
        for bucketID in [leaf] + self.getPathNodes(leaf):
            if leaf in self._buckets[bucketID-1]:
                self._buckets[bucketID-1].index(leaf) == 0
                return 1				
        return 0				
				
    def getPathNodes(self, leaf):
        result = []
        leaf = leaf >> 1 #the leaf itself is NOT in the returned list
        while (leaf>0):
            result.insert(0,leaf)
            leaf = leaf>>1
        return result
    
    def getMaxLevel(self, leaf1, leaf2):
    #print (str(leaf1) + " and " + str(leaf2))
        if leaf1 == 1 or leaf2 == 1:
            return 0
        
        if self.levelNumber(leaf1) > self.levelNumber(leaf2):
            return self.levelNumber(leaf1)
            leaf1 = leaf1 >> 1
        elif self.levelNumber(leaf1) < self.levelNumber(leaf2):
            return self.levelNumber(leaf2)
            leaf2 = leaf2>>1
        if leaf1==leaf2:
            return self.levelNumber(leaf1); 
        
        
        
        
        
        
