from typing import TypeVar
T = TypeVar('T')

class Node:
    def __init__(self, value: T):
        '''
        initial constructor
        '''
        self.value : T = value
        self.weight : int = 1
        self.left : Node = None
        self.right : Node = None
        self.parent : Node = None

# =================== TESTS BOOLEENS ===================
    def isLeaf(self) -> bool:
        '''returns true if the given node is a leaf'''
        return (not self.left and not self.right) # pas de fils g et d 

    def isNode(self) -> bool:
        '''returns true if the given node is a node (ie : parent of (at least) another node OR parent of (AL) leaf)'''
        return (self.left or self.right) # au moins un fils g ou d
    
    def isRoot(self) -> bool:
        '''returns true if the given node is the root of the tree'''
        return not(self.parent) # self.parent == none : pas de parent => racine de l'arbre
    

# =================== CHILDS CTORS ===================
    def newLeft(self, value: T) -> "Node":
        if (self.left == None): # possible d'avoir deja un node left
            self.left = Node(value)
            self.left.parent = self
            return self.left

    def newRight(self, value: T) -> "Node":
        if (self.right == None): # possible d'avoir deja un node right
            self.right = Node(value)
            self.right.parent = self
            return self.right


# =================== GETTERS ===================
    def getValue(self) -> T:
        """retourne la value du noeud actuel"""
        return self.value
    
    def getWeight(self) -> int:
        """retourne le weight du noeud actuel"""
        return self.weight
    

# =================== UTILS ===================
    def searchNode(self, value : T, searchAll : bool = False, verbose : bool = False) -> "Node" :
        """Cherche une valeur dans l'arbre. Renvoie le node ou None si non présent"""
        
        if (self.isLeaf() or searchAll):
            if (self.value == value) :
                if verbose:
                    print(f"getNode : node avec valeur {self.value} trouvé")
                return self
        
        left : Node = self.left.searchNode(value, searchAll, verbose) if self.left else None
        right : Node = self.right.searchNode(value, searchAll, verbose) if self.right else None

        if left :
            return left
        return right
    
    
# =================== MISCS ===================
    def length(self) -> int:
        '''returns length from the given tree (node to bttm)'''
        if self.isLeaf():
            return 1
        lenLeft = self.left.length() if self.left else 0 # cas d'appel sur un node None => pas de méthode length
        lenRight = self.right.length() if self.right else 0
        return max(lenLeft, lenRight) +1
    
    def distFromRoot(self) -> int:
        if self.isRoot():
            return 0
        return self.parent.distFromRoot() +1


    def __str__(self):
        '''Affichage joli de l'arbre avec des lignes ASCII'''
        def _build_tree_lines(node, prefix="", is_tail=True):
            """Construit les lignes d'affichage de l'arbre récursivement"""
            if node is None:
                return []
            
            lines = []
            # Ligne pour le noeud actuel
            connector = "└── " if is_tail else "├── "
            lines.append(prefix + connector + f"{node.value} (w:{node.weight})")
            
            # Préparer le préfixe pour les enfants
            extension = "    " if is_tail else "│   "
            new_prefix = prefix + extension
            
            # Traiter les enfants (d'abord le droit, puis le gauche pour l'affichage correct)
            children = []
            if node.right:
                children.append(('right', node.right))
            if node.left:
                children.append(('left', node.left))
            
            for i, (_, child) in enumerate(children):
                is_last = (i == len(children) - 1)
                lines.extend(_build_tree_lines(child, new_prefix, is_last))
            
            return lines
        
        # Cas spécial pour la racine
        if self.isRoot():
            lines = [f"{self.value} (w:{self.weight})"]
            children = []
            if self.right:
                children.append(self.right)
            if self.left:
                children.append(self.left)
            
            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                lines.extend(_build_tree_lines(child, "", is_last))
            
            return "\n".join(lines)
        else:
            # Si ce n'est pas la racine, on l'affiche quand même
            return "\n".join(_build_tree_lines(self, "", True))
        
        
# =================== PARCOURS ===================
    def getLeftNeighbor(self, high : int = 0, verbose :  bool = False) -> "Node":
        """retourne le noeud à gauche sur la même ligne"""
        print(f"Exploration node {self.value} (high={high})\n") if verbose else None
        if self.isRoot():
            return None
        if (self.parent.isRoot()) and (self.parent.left==self): # on cherche un voisin gauche alors qu'on est le + à gauche
            print(f"node {self.value} est le fils gauche du root") if verbose else None
            return None
        if (self == self.parent.left):
            print("On monte dans l'arbre") if verbose else None
            high += 1
            return self.parent.getLeftNeighbor(high, verbose)
        else :
            print(f"On va au fils gauche du parent puis on redescend {high} fois à droite") if verbose else None
            current : Node = self.parent.left
            # Descendre à droite autant de fois que nécessaire (high fois)
            for _ in range(high):
                if current.right is None:
                    print(f"Impossible de descendre plus") if verbose else None
                    return None
                current = current.right
                print(f"Descente -> {current.value}") if verbose else None
            return current
        
    def getRightNeighbor(self, high : int = 0, verbose :  bool = False) -> "Node":
        """retourne le noeud à droite sur la même ligne"""
        print(f"Exploration node {self.value} (high={high})\n") if verbose else None
        if self.isRoot():
            return None
        if (self.parent.isRoot()) and (self.parent.right==self): # on cherche un voisin gauche alors qu'on est le + à gauche
            print(f"node {self.value} est le fils droit du root") if verbose else None
            return None
        if (self == self.parent.right):
            print("On monte dans l'arbre") if verbose else None
            high += 1
            return self.parent.getRightNeighbor(high, verbose)
        else :
            print(f"On va au fils droit du parent puis on redescend {high} fois à gauche") if verbose else None
            current : Node = self.parent.right
            # Descendre à droite autant de fois que nécessaire (high fois)
            for _ in range(high):
                if current.left is None:
                    print(f"Impossible de descendre plus") if verbose else None
                    return None
                current = current.left
                print(f"Descente -> {current.value}") if verbose else None
            return current

        

    def GDBH(self)-> list["Node"]:
        '''renvoie le parcours GDBH jusqu'à la racine du node concerné'''
        pass


if __name__=="__main__":
    print("Node")