from .Node import Node
from typing import List
from bitarray import bitarray

def swapNodes(nodeA : Node, nodeB : Node, verbose : bool = False) -> None:
    if verbose :
        # print(("="*20)+" Swapping: "+ ("="*20) + "\n"
        #     + str(nodeA) +
        #     "\n\n\t<->\n\n" 
        #     + str(nodeB) + "\n" 
        #     + ("="*50) + "\n")
        print(f"-- Swap entre {nodeA.value}:{nodeA.weight} et {nodeB.value}:{nodeB.weight}")
        
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
def lecture(file : str) -> bitarray:
    """Lit un fichier et renvoie un bitarray"""
    bits = bitarray()
    with open(file, 'rb') as f:
        bits.fromfile(f)
    
    return bits

def cutBin(bin : bitarray) -> List[bitarray]:
    """Découpe un bitarray UTF-8 en plusieurs caractères (bitarrays individuels).
    Si des bits restants ne forment pas un octet complet, ils sont complétés avec des 0."""
    result = []
    i = 0
    
    while i < len(bin):
        # Vérifier le premier octet pour déterminer le nombre d'octets du caractère
        if i + 8 > len(bin):
            # Pas assez de bits pour un octet complet -> compléter avec des 0
            remaining = bin[i:]
            padding_needed = 8 - len(remaining)
            padded = remaining + bitarray('0' * padding_needed)
            result.append(padded)
            break
        
        first_byte = bin[i:i+8]
        
        # ASCII > code 1 octet (premier bit à 0)
        if not first_byte[0]:  # bit à 0
            result.append(bin[i:i+8])
            i += 8
        # 2 premiers bits à 1 > code sur 2 octets 
        elif first_byte[0] and first_byte[1] and not first_byte[2]:  # pattern 110
            if i + 16 <= len(bin):
                result.append(bin[i:i+16])
                i += 16
            else:
                # Pas assez de bits pour 2 octets -> compléter avec des 0
                remaining = bin[i:]
                padding_needed = 16 - len(remaining)
                padded = remaining + bitarray('0' * padding_needed)
                result.append(padded)
                break
        # 3 premiers bits à 1 > code sur 3 octets
        elif first_byte[0] and first_byte[1] and first_byte[2] and not first_byte[3]:  # pattern 1110
            if i + 24 <= len(bin):
                result.append(bin[i:i+24])
                i += 24
            else:
                # Pas assez de bits pour 3 octets -> compléter avec des 0
                remaining = bin[i:]
                padding_needed = 24 - len(remaining)
                padded = remaining + bitarray('0' * padding_needed)
                result.append(padded)
                break
        # 4 premiers bits à 1 > code sur 4 octets
        elif first_byte[0] and first_byte[1] and first_byte[2] and first_byte[3] and not first_byte[4]:  # pattern 11110
            if i + 32 <= len(bin):
                result.append(bin[i:i+32])
                i += 32
            else:
                # Pas assez de bits pour 4 octets -> compléter avec des 0
                remaining = bin[i:]
                padding_needed = 32 - len(remaining)
                padded = remaining + bitarray('0' * padding_needed)
                result.append(padded)
                break
        else:
            # cas de caractères sur plus de 4 octets : on ne les gère pas
            i += 8
    
    return result

def decodeBin(bin : bitarray) -> str:
    """Décode un bitarray en string UTF-8"""
    return bin.tobytes().decode('utf-8')

def toBin(bin : bitarray) -> bytes:
    """Convertit un bitarray en bytes"""
    return bin.tobytes()

def writeBin(bin : bitarray, file : str):
    """Écrit un bitarray dans un fichier binaire"""
    with open(file, 'wb') as f:
        bin.tofile(f)

