import Node

def swapNodes(nodeA : Node, nodeB : Node) -> None:
    print(("="*20)+" Swapping: "+ ("="*20) + "\n"
          + str(nodeA) +
          ("\t"*3)+"<->\t" 
          + str(nodeB) + "\n" 
          + ("="*50) + "\n")
        
    # swap values and weights
    nodeA.value, nodeB.value = nodeB.value, nodeA.value
    nodeA.weight, nodeB.weight = nodeB.weight, nodeA.weight
    # swap children
    nodeA.left, nodeB.left  = nodeB.left, nodeA.left
    nodeA.right, nodeB.right  = nodeB.right, nodeA.right
    # update childrens parents (if was internal node, not the case in huffman)
    if nodeA.left: 
        nodeA.left.parent = nodeA
    if nodeA.right:
        nodeA.right.parent = nodeA
    if nodeB.left:
        nodeB.left.parent = nodeB
    if nodeB.right:
        nodeB.right.parent = nodeB


def createTree(root : "Node", length : int) -> Node:
    if length >0 :
        left = root.newLeft(2*root.getValue()+1)
        createTree(left, length-1)

        right = root.newRight(2*root.getValue()+2)
        createTree(right, length-1)

    return root