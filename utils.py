import Node
from typing import List

def swapNodes(nodeA : Node, nodeB : Node, verbose : bool = False) -> None:
    if verbose :
        print(("="*20)+" Swapping: "+ ("="*20) + "\n"
            + str(nodeA) +
            "\n\n\t<->\n\n" 
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


# =================== GESTION FICHIERS BINAIRES ===================
def lecture(file : str) -> str:
    """lit un fichier utf-8 et renvoie une string binaire"""
    with open(file, 'rb') as f:
        contenu = f.read()

    bits = ''.join(format(byte, '08b') for byte in contenu)
    return bits

def cutBin(bin : str) -> List[str]:
    """cut une chaine binaire utf8 en plusieurs lettres binaires"""
    result = []
    i = 0
    
    while i < len(bin):
        # Vérifier le premier octet pour déterminer le nombre d'octets du caractère
        if i + 8 > len(bin):
            break  # Pas assez de bits restants
        
        first_byte = bin[i:i+8]
        
        # ASCII > code 1 octet (premier bit à 0)
        if first_byte[0] == '0':
            result.append(bin[i:i+8])
            i += 8
        # 2 premiers bits à 1 > code sur 2 octets 
        elif first_byte[:3] == '110':
            if i + 16 <= len(bin):
                result.append(bin[i:i+16])
                i += 16
            else:
                break
        # 3 premiers bits à 1 > code sur 3 octets
        elif first_byte[:4] == '1110':
            if i + 24 <= len(bin):
                result.append(bin[i:i+24])
                i += 24
            else:
                break
        # 4 premiers bits à 1 > code sur 4 octets
        elif first_byte[:5] == '11110':
            if i + 32 <= len(bin):
                result.append(bin[i:i+32])
                i += 32
            else:
                break
        else:
            # cas de caractères sur plus de 4 octets : on ne les gère pas
            i += 8
    
    return result

def decodeBin(bin : str) -> str:
    byte_length = (len(bin) + 7) // 8
    bin_bytes = int(bin, 2).to_bytes(byte_length, byteorder='big')
    return bin_bytes.decode()

def lectureBin(file : str):
    pass

def writeBin(bin : bytes, file : str):
    with open(file, 'wb') as f:
        f.write(bin)

