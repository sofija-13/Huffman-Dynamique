from .Node import Node
from typing import List, TypeVar
from bitarray import bitarray

def swapNodes(nodeA : Node, nodeB : Node, verbose : bool = False) -> None:
    """_Swap deux nodes. Modification des pointeurs dans l'arbre_
    Args:
        nodeA (Node): _Premier node à swap_
        nodeB (Node): _Deuxième node à swap_
        verbose (bool, optional): _Verbose_. Defaults to False.\\
    """
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
    """_Crée un arbre binaire de longueur définie de la forme lectureGDHB=1,2,3..._
    Args:
        root (Node): _Premier node (racine) utilisé à la création_
        length (int): _Longueur de l'arbre souhaité _
    Returns:
        Node: _La racine de l'arbre_\\
    """
    if length >0 :
        left = root.newLeft(2*root.getValue()+1)
        createTree(left, length-1)

        right = root.newRight(2*root.getValue()+2)
        createTree(right, length-1)
    return root


def updateWeights(node : Node, verbose : bool = False) -> None:
    """_Met à jour les poids des noeuds internes de l'arbre. \\
    Parcours l'arbre vers le haut à partir de noeud node_
    Args:
        node (Node): Noeud de l'arbre de Huffman. 
    Returns : 
        None : mise à jour de l'arbre de manière in-place\\
    """
    current : Node = node.parent if node.parent else node
    print(f"updateWeights à partir de {current.value},{current.weight}") if verbose else None
    while current is not None:
        if current.left and current.right:
            current.weight = current.left.weight + current.right.weight
        if current.isRoot():
            break
        current = current.parent
    return

T = TypeVar('T')
def newNode(NYT : Node, value : T) -> Node:
    """Insère une nouvelle valeur dans l'arbre de Huffman à partir de son NYT
    Args:
        NYT (Node): Le noeud # de l'arbre de Huffman
        value (T): La valeur du nouveau noeud à insérer dans l'arbre  
    Returns:
        Node : le nouveau pointeur vers NYT (#)\\
    """
    oldNYT : Node = NYT
    oldNYT.weight = 1
    oldNYT.value = None 
    oldNYT.left = Node("#", weight=0)
    oldNYT.right = Node(value)
    
    oldNYT.left.parent = oldNYT
    oldNYT.right.parent = oldNYT
    
    return oldNYT.left 

def updateSwap(node : Node, root : Node, verbose : bool = False)->int:
    """Met à jour la forme de l'arbre pour respecter le principe d'arbre de Huffman (p(w1)<=p(w2) dans l'ordre GDBH)
    Args:
        node (Node): Le noeud nouvellement inséré/mis à jour dans l'arbre
        root (Node): La racine de l'arbre
        verbose (bool, optional): Mode verbose. Defaults to False.
    Returns:
        int : 1 si une update a eu lieu, 0 si aucune update\\
    """
    # [2,2,2,3,3,3,3,1,1,1,3]
    #        |           |
    
    parcours : List[Node] = node.GDBH(root)
    current : Node = parcours[0]
    for i in range(len(parcours)):
        if (parcours[i].weight > current.weight) : #nouveau poids
            current = parcours[i]
            # print(f"update current weight: {current.weight}")
        elif (parcours[i].weight < current.weight): #problème (poids actuel > poids suivant)
            j : int = i
            # print(f"probleme node {i} weight {parcours[i].weight}")
            while (j<len(parcours) and parcours[j].weight<parcours[i-1].weight):
                # print(f"problème id {j}")
                j+=1
            # print(f"swap entre nodes {parcours[i].value},{parcours[i].weight} et {parcours[j].value},{parcours[j].weight}")
            swapNodes(current, parcours[j-1], verbose)
            updateWeights(parcours[j-1])
            updateWeights(current)
            return 1
    print("pas de swap") if verbose else None
    return 0

def encode(text : str, verbose : bool = False)->bitarray:
    """_Compresse un texte de format UTF-8 par l'algorithme de Huffman Adaptatif_
    Args:
        text (str): le texte de base en format UTF-8
        verbose (bool, optional): Mode verbose. Defaults to False.
    Returns:
        bitarray: le texte compressé en format bitarray\\
    """
    
    # Arbre vide au départ
    NYT : Node = Node("#", weight=0)
    root : Node = NYT #pointeur sur le haut de l'arbre à chaque fois
    # Résultat
    # res : bitarray = bitarray()
    res : str = ""
    for lettre in text :
        search : Node = root.searchNode(lettre, verbose=verbose)
        
        if search : #cas où la lettre lue est déjà dans l'arbre
            print(f"Lettre {lettre} trouvée") if verbose else None
            search.weight += 1
            update : Node = search
            print(f"Update de {lettre}") if verbose else None
            print(root) if verbose else None
            
        else : #cas où la lettre lue n'est pas encore dans l'arbre 
            print(f"Lettre {lettre} non trouvée") if verbose else None
            NYT = newNode(NYT, lettre) # insertion de la nouvelle lettre
            update : Node = NYT
            print(f"Ajout de {lettre}") if verbose else None
            print(root) if verbose else None
            
        updateWeights(update)
        print(f"Update des poids") if verbose else None
        print(root) if verbose else None
        res = 1
        while (res==1): #swap des nodes qui fail le gdbh tant qu'il y en a 
            res = updateSwap(update, root, verbose)
        # updateWeights(update)
        print(f"--Rendu final près ajout de {lettre} :") if verbose else None
        print(root) if verbose else None
        print("\n"+"="*20) if verbose else None
            
    print(root)  


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
        