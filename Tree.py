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
    
    def clearBucket(self, bucketID):
        self._buckets[bucketID - 1] = [0 for i in range(self._z)]
        return
        
    def setBucket(self, bucketID, contents):
        self._buckets[bucketID - 1] = contents
        return
    
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


         
    def eviction(self):
        
        nextLeaf = RLOLeaf()
        leaves=getPathNodes(nextLeaf)
        for i in range(len(leaves)):

            curBucket=leaves[i]
            getBucket(2*(i+1))=merge(leaves[i],getBucket(2*(i+1)))
            getBucket(2*(i+1)+1=merge(leaves[i],getBucket(2*(i+1)+1))

            for j in range(len(curBucket):
                curBucket[j]=0



      
     

    def mergeNodes(node1, node2): #merge functions using the TreeNode representation
        newnode = merge(node1, node2)
        #update/account for noisy blocks
        
        return newnode

            
    def AssignFromList(self, objnum, locs): #randomly assigns objects locations from specified list
        
        assert(objnum <= len(locs)), "Pigeon-hole Principle Violation"
        
        mapping = []
        
        for i in range(objnum):
            
            newloc = locs[random.randint(0,len(locs) - 1)]
            mapping.append(newloc)
            locs.remove(newloc)
        
        
        return [mapping, locs]
    
    def levelNumber(self, bucket):#returns the level a leaf is on (used in getMaxLevel)
        a = int(math.log(bucket,2))
        if(leaf == 2**a):
            return a
        return a
    
    def children(self, bucketID): 
        assert(levelNumber(bucketID) < self._height - 1), "Leaves have no children"
        
        return [2 * bucketID, 2 * bucketID + 1] #IDs of children
    
    def evictToKids(self, bucketID):
        
        kids = children(bucketID)
        
        kidContents = [mergeNodes(self.getBucket(kids[0]),self.getBucket(bucketID)), 
                mergeNodes(self.getBucket(kids[1]),self.getBucket(bucketID))]
        
        self.clearBucket(BucketID)
        
        self.setBucket(kids[0], kidContents[0])
        self.setBucket(kids[1], kidContents[1])
        
        return
    
    def evictAll(self, input):
        self.setBucket(1, input)
        
        evictees = getPathNodes(self.RLOLeaf())
        
        for node in evictees:
            self.evictToKids(node)
            
        return
    
    def getPathNodes(leaf):
        result = []
        leaf = leaf >> 1 #the leaf itself is NOT in the returned list
        while (leaf>0):
            result.insert(0,leaf)
            leaf = leaf>>1
        return result
        
        
        
        
        
        
