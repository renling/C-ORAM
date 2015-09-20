from Tree import Tree
import math
import random
import time

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
def counter():
    Tree.seed = Tree.seed + 1
    return Tree.seed

def testMerge(testnum):
    ORAMsize = (1 << 7) - 1
    z = 5000
    
    maxR = 250
    maxN = 250
    
    
    t = Tree(ORAMsize, z)
    
    numpassed = 0

    start = time.clock()
    

    for i in range(testnum):
        passed = True
       
        rrand1 = random.randint(0, maxR)
        nrand1 = random.randint(0, maxN)
        rrand2 = random.randint(0, maxR)
        nrand2 = random.randint(0, maxN)
        
        b1 = [-1 for j in range(nrand1)] 
        b1 += [counter() for j in range(rrand1)]
        b1 += [0 for j in range(z - rrand1 - nrand1)]
        b2 = [-1 for j in range(nrand2)] 
        b2 += [counter() for j in range(rrand2)]
        b2 += [0 for j in range(z - rrand2 - nrand2)]
        
        
        #print("Testing " + str(i + 1) + " of " + str(testnum))
        temp = b1
        #print(b1)
        #print(b2)
        res = t.merge(b1, b2)
        #print(res)
        #print("")
        
        conts = countTypes(res)
        
        if conts[0] != rrand1 + rrand2:
            passed = False
            print("Expected " + str(rrand1 + rrand2) + " real blocks, found " + str(conts[0]))
        
        if conts[1] != max(nrand1, nrand2):
            passed = False
            print("Expected " + str(max(nrand1, nrand2)) + " noisy blocks, found " + str(conts[1]))
        
        if(passed != False):
            numpassed += 1
        else:
            print(temp)
            print(b2)
            print(res)
            
    timetaken = time.clock() - start       
         
    if(numpassed == testnum):
        print("Test Merge PASSED!")
    
    else:
        print("Test Merge FAILED! (" + str(numpassed) + " of " + str(testnum) + " passed)")
    
    print("Took %.2f seconds" % timetaken)
    
        
def testEvict():
    ORAMsize = (1 << 4) - 1
    z = 10
    t = Tree(ORAMsize, z)
    exp = 5
    
    leaves = t._leaves
    
    input = random.sample(leaves, exp)
    
    start = time.clock()
    
    t.evictAll(input)
    for i in range(ORAMsize):
        print("Eviction " + str(i) + " of " + str(ORAMsize))
        t.evictAll([0 for i in range(z)])
    
    timetaken = time.clock() - start
    
    reals = 0
    safety = 0
    
    for leaf in range(ORAMsize):
        safety = safety + countTypes(t.getBucket(leaf))[0]
        
    for leaf in t._leaves:
        reals = reals + countTypes(t.getBucket(leaf))[0]

    
    print(str(reals) + '/' + str(exp) + ' found')
    if reals == exp and reals == safety:
        print("TEST EVICTION PASSED")
    else:
        print("TEST EVICTION FAILED")
    
    print("Took %.2f seconds" % timetaken)
    
    #print(t._buckets)
    # fill in once we have some more structure
    #commit?

def timeEvict():
    ORAMsize = (1 << 13) - 1
    z = 4000
    
    start = time.clock()
    
    t = Tree(ORAMsize, z)
    
    timetaken = time.clock() - start
    print("Took %.4f seconds to create tree" % (timetaken))
    
    exp = 10
    
    leaves = t._leaves
    
    input = random.sample(leaves, exp)
    
    num = 400 #number of tests to average
    
    for i in range(num/10):
        start = time.clock()
        
        for i in range(10):
            input = random.sample(leaves, exp)
            t.evictAll(input)
            #print(t._buckets)
        
        timetaken = time.clock() - start
        
        print("%.2f" % (timetaken/10))

def testRate(freq): #freq is an integer (A)
    l = 10
    
    ORAMsize = (1 << l) - 1
    z = 1000
    
    t = Tree(ORAMsize, z)
    
    exp = l
    
    leaves = t._leaves
    
    
    for i in range(int(500/l)):
        input = random.sample(leaves, exp)
        t.evictAll(input)
    
    counter = 0
    
    while True:
        
        for i in range(int(exp * freq)):
            t.removeRand()
        
        input = random.sample(leaves, exp)
        print(input)
        t.evictAll(input)
        
        counter = counter + 1
        print(str(counter) + " successful removal/eviction cycles")
        

def countTypes(bucket): #returns counts of [real, noisy, zero]
    
    nCount = 0
    rCount = 0
    zCount = 0
    
    for i in range(len(bucket)): #gathers metadata
        
        if(bucket[i] == 0):
            zCount += 1
            
        if(bucket[i] == -1):
            nCount += 1
            
        if(bucket[i] >= 1):
            rCount += 1
            
    return [rCount, nCount, zCount]

def testOverflow():
    ORAMsize = (1 << 10) - 1
    z = 1000
    t = Tree(ORAMsize, z)
    exp = 10
    
    
    leaves = t._leaves
    counter = 0
    
    while True:
            input = random.sample(leaves, exp)
            t.evictAll(input)
            counter = counter + 1
            print(str(counter) + " evictions of " + str(exp) + " blocks completed")
#testMerge(10000)
#timeEvict()
#testRate(15)
testOverflow()