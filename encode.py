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
    
# 00111111000000111111001110110000001111100000010110000111010100011101010111100110011110110010111011100010001110011000110101011110110010110010110010000
# 001111110000001111110011101100000011111000000101100001110101000111010101111001100111101100101110111000100011100110001101010111101100101100101100100000000

# 011100110001101010111101100101100101100100000000
# 01110011000110101011110110010110010110010000