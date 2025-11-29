#! python3

import sys
from src.utils import encode, writeBin

def main():
    if len(sys.argv) != 3:
        print("Usage: python encode.py <fichier_entree> <fichier_sortie>")
        sys.exit(1)
    elif (sys.argv[1]==sys.argv[2]):
        print("⚠️ Les fichiers d'entrée et sortie doivent être différents")
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        contenu = f.read()
    
    writeBin(encode(contenu), sys.argv[2])
    print(f"Fichier encodé avec succès: {sys.argv[1]} -> {sys.argv[2]}")

if __name__ == "__main__":
    main()
