from Tree import Tree
import math
import random


def testRLO(): #tests that RLO is working by generating all RLO values
    ORAMsize = (1 << 7) - 1
    z = 5
    
    t = Tree(ORAMsize, z)
    
    leaves = []
    
    for i in range(ORAMsize):
        leaves.append(t.RLOLeaf())
    
    print(leaves)
        
    leaves.sort()
    
    print(leaves)

def testMerge(testnum):
    ORAMsize = (1 << 7) - 1
    z = 5000
    
    maxR = 250
    maxN = 250
    
    
    t = Tree(ORAMsize, z)
    
    numpassed = 0
    passed = True
    
    for i in range(testnum):
        
        rrand1 = random.randint(0, maxR)
        nrand1 = random.randint(0, maxN)
        rrand2 = random.randint(0, maxR)
        nrand2 = random.randint(0, maxN)
        
        b1 = [-1 for j in range(nrand1)] 
        b1 += [1 for j in range(rrand1)]
        b1 += [0 for j in range(z - rrand1 - nrand1)]
        b2 = [-1 for j in range(nrand2)] 
        b2 += [1 for j in range(rrand2)]
        b2 += [0 for j in range(z - rrand2 - nrand2)]
        
        
        print("Testing " + str(i + 1) + " of " + str(testnum))
        print(b1)
        print(b2)
        res = t.merge(b1, b2)
        print(res)
        print("")
        
        conts = countTypes(res)
        
        if conts[0] != rrand1 + rrand2:
            passed = False
            print("Expected " + str(rrand1 + rrand2) + " real blocks, found " + str(conts[0]))
        
        if conts[1] != max(nrand1, nrand2):
            passed = False
            print("Expected " + str(max(nrand1, nrand2)) + " noisy blocks, found " + str(conts[1]))
        
        if(passed != False):
            numpassed += 1
        
    if(numpassed == testnum):
        print("Test Merge PASSED!")
    
    else:
        print("Test Merge FAILED! (" + str(numpassed) + " of " + str(testnum) + " passed)")
        
def testEvict():
    ORAMsize = (1 << 7) - 1
    # fill in once we have some more structure

def countTypes(bucket): #returns counts of [real, noisy, zero]
    
    nCount = 0
    rCount = 0
    zCount = 0
    
    for i in range(len(bucket)): #gathers metadata
        
        if(bucket[i] == 0):
            zCount += 1
            
        if(bucket[i] == -1):
            nCount += 1
            
        if(bucket[i] == 1):
            rCount += 1
            
    return [rCount, nCount, zCount]


testMerge(100)