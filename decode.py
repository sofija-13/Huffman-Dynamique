#! python3
import sys
from src.utils import decode, writeStr, lecture

def main():
    if len(sys.argv) != 3:
        print("Usage: python decode.py <fichier_entree> <fichier_sortie>")
        sys.exit(1)
    elif (sys.argv[1]==sys.argv[2]):
        print("⚠️ Les fichiers d'entrée et sortie doivent être différents")
        sys.exit(1)
        
    contenu : bitarray = lecture(sys.argv[1])
    
    writeStr(sys.argv[2], decode(contenu))
    print(f"Fichier encodé avec succès: {sys.argv[1]} -> {sys.argv[2]}")

if __name__ == "__main__":
    main()