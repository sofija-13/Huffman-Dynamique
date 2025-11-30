from .Node import Node
from typing import List, TypeVar, Set, Tuple
from bitarray import bitarray

def swapNodes(nodeA : Node, nodeB : Node, verbose : bool = False) -> None:
    """_Swap deux nodes. Modification des pointeurs dans l'arbre_
    Args:
        nodeA (Node): _Premier node à swap_
        nodeB (Node): _Deuxième node à swap_
        verbose (bool, optional): _Verbose_. Defaults to False.\\
    """
    if verbose :
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
        left = root.newLeft(2*root.value+1)
        createTree(left, length-1)

        right = root.newRight(2*root.value+2)
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
    oldNYT.left = Node("##", weight=0)
    oldNYT.right = Node(value)
    
    oldNYT.left.parent = oldNYT
    oldNYT.right.parent = oldNYT
    
    return oldNYT.left 

def getCode(root : Node, value : T, verbose : bool = False) -> bitarray:
        """_Renvoie le code du parcours correspondant à une valeur_
        Args:
            root (Node): _Racine de l'arbre contenant la valeur_
            value (T): _Valeur dont on souhaite obtenir le code_
        Returns:
            bitarray: _Si valeur présente dans l'arbre, le code lui correspondant._\\
        """

        if root.isLeaf():
            if root.value == value:
                return bitarray()
            return None

        if root.left:
            res = getCode(root.left, value)
            if res is not None:
                return bitarray('0') + res

        if root.right:
            res = getCode(root.right, value)
            if res is not None:
                return bitarray('1') + res

        return None

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
            return updateSwap(node, root, verbose)
    print("pas de swap") if verbose else None
    return 0

def avance(node : Node, bit : int)-> Node:
    if (node == None):
        return None
    elif (bit == 1): # 1
        return node.right
    else:
        return node.left

def encode(text : str, verbose : bool = False)->bitarray:
    """_Compresse un texte de format UTF-8 par l'algorithme de Huffman Adaptatif_
    Args:
        text (str): le texte de base en format UTF-8
        verbose (bool, optional): Mode verbose. Defaults to False.
    Returns:
        bitarray: le texte compressé en format bitarray\\
    """
    # Arbre vide au départ
    NYT : Node = Node("##", weight=0)
    root : Node = NYT #pointeur sur le haut de l'arbre à chaque fois
    # Résultat
    res : bitarray = bitarray()
    # res : str = ""
    for lettre in text :
        search : Node = root.searchNode(lettre, verbose=verbose)
        
        if search : #cas où la lettre lue est déjà dans l'arbre
            print(f"Lettre {lettre} trouvée") if verbose else None
            code : bitarray = getCode(root, lettre)
            res += code
            # print(f"\tres {res}")
            search.weight += 1
            update : Node = search
            print(f"Update de {lettre}") if verbose else None
            print(root) if verbose else None
            
        else : #cas où la lettre lue n'est pas encore dans l'arbre 
            print(f"Lettre {lettre} non trouvée") if verbose else None
            code : bitarray = getCode(root, "##")
            res = res + code
            res.frombytes(lettre.encode('utf-8')) #ajout de la lettre aux bits
            NYT = newNode(NYT, lettre) # insertion de la nouvelle lettre
            update : Node = NYT
            print(f"Ajout de {lettre}") if verbose else None
            print(root) if verbose else None
            
        updateWeights(update)
        print(f"Update des poids") if verbose else None
        print(root) if verbose else None
        cond = 1
        updateSwap(update, root, verbose)
        # updateWeights(update)
        print(f"--Rendu final près ajout de {lettre} :") if verbose else None
        print(root) if verbose else None
        print("\n"+"="*20) if verbose else None
            
    # Ne pas ajouter de padding ici; on stocke la longueur utile séparément
    return res

def decode(code : bitarray, verbose : bool = False)-> str:
    """_Décompresse un fichier encodé par l'algorithme de Huffman Adaptatif_
    Args:
        code (bitarray): _Texte encodé en binaire_
        verbose (bool, optional): Mode verbose. Defaults to False.
    Returns:
        str: _Le texte décodé en UTF-8_
    """
    
    # Arbre vide au départ
    NYT : Node = Node("##", weight=0)
    root : Node = NYT #pointeur sur le haut de l'arbre à chaque fois
    # Résultat - les premiers bits correspondent toujours à un symbole
    (res, code) = readUTF8(code) # décode le premier symbole
    if res == "??" or code is None:
        return ""
    NYT = newNode(NYT, res) #res contient un seul caractère
    print(root) if verbose else None

    while (code and len(code)):
        if code.count(1) == 0:
            break  # le reste n'est que du padding (zéros)
        avancement : Node = root
        while (not avancement.isLeaf()):
            if len(code) == 0:
                break
            avancement = avance(avancement, code[0])
            code = code[1:]

        if not avancement.isLeaf():
            break

        if (avancement == NYT):
            print(f"lettre non trouvée {code[:8]}") if verbose else None
            decoded : str
            (decoded, code) = readUTF8(code)
            if decoded == "??" or code is None:
                break  # Arrêter la boucle si padding ou fin
            NYT = newNode(NYT, decoded)
            print(f"ajout symbole {decoded}") if verbose else None
            res = res + decoded
        else:
            print(f"lettre trouvée {avancement}") if verbose else None
            avancement.weight += 1
            res = res + avancement.value
            print(f"increased {avancement.value}") if verbose else None

        print(f"{root}\n") if verbose else None
        updateWeights(avancement)
        updateSwap(avancement, root)

    print(root) if verbose else None
    return res


# =================== GESTION FICHIERS BINAIRES ===================
def lecture(file : str) -> bitarray:
    """Lit un fichier binaire et renvoie un bitarray"""
    bits = bitarray()
    with open(file, 'rb') as f:
        bits.fromfile(f)
    
    return bits

def readUTF8(bin : bitarray) -> (str, bitarray):
    """Découpe un bitarray UTF-8 en plusieurs caractères (bitarrays individuels).
    Si des bits restants ne forment pas un octet complet, ils sont complétés avec des 0.

    Retourne une liste où chaque élément est un bitarray représentant un caractère
    complet UTF-8 (1 à 4 octets). Le dernier élément est padding si incomplet."""
    
    if len(bin) < 8: #on a pas un bit entier restant
        return ("??", None)

    # Déterminer la longueur UTF-8 à partir des bits de tête
    # 0xxxxxxx -> 1 octet
    # 110xxxxx -> 2 octets
    # 1110xxxx -> 3 octets
    # 11110xxx -> 4 octets
    if not bin[0]:
        char_bits_len = 8
    elif bin[0] and bin[1] and not bin[2]:
        char_bits_len = 16
    elif bin[0] and bin[1] and bin[2] and not bin[3]:
        char_bits_len = 24
    elif bin[0] and bin[1] and bin[2] and bin[3] and not bin[4]:
        char_bits_len = 32
    else:
        print("Symbole ne respecte pas utf-8")
        return ("??", None)
    
    reste : bitarray = bin[char_bits_len:]
    result : str = bin[:char_bits_len].tobytes().decode('utf-8')

    return (result, reste)

def writeStr(file : str, buffer : str)->None:
    with open(file, "w") as f:
        f.write(buffer)

def writeBin(bin : bitarray, file : str):
    """Écrit un bitarray dans un fichier binaire"""
    with open(file, 'wb') as f:
        bin.tofile(f)

def ecriture(fichier_chaine : str, fichier : str) -> str:
    """Encode le texte fichier_chaine 
    sous forme de fichier binaire"""
    bin = lecture(fichier_chaine)
    with open('fichier.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        bin.frombytes(text.encode('utf-8'))
        bin.tofile(f)    
    
    return fichier