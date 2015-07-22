from Tree import Tree


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


testRLO()