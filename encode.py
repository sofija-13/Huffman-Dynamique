#! python3

import sys, os, time
from src.utils import encode, writeBin

def infos_compression(txt_path, bin_path, temps):
    txt_size = os.path.getsize(txt_path) if os.path.exists(txt_path) else 0
    bin_size = os.path.getsize(bin_path) if os.path.exists(bin_path) else 0
    taux_comp = bin_size / txt_size
    #taux = 1 - ratio
    #facteur = txt_size / bin_size
    print(f"{txt_path};{bin_path};{txt_size};{bin_size};{taux_comp:.5%};{temps}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python encode.py <fichier_entree> <fichier_sortie>", file=sys.stderr)
        sys.exit(1)
    elif (sys.argv[1]==sys.argv[2]):
        print("⚠️ Les fichiers d'entrée et sortie doivent être différents", file=sys.stderr)
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        contenu = f.read()

    temps_debut = time.time()
    encoded = encode(contenu)
    temps_fin = time.time()
    writeBin(encoded, sys.argv[2])
    print(f"Fichier encodé avec succès: {sys.argv[1]} -> {sys.argv[2]}", file=sys.stderr)
    infos_compression(sys.argv[1], sys.argv[2], temps_fin-temps_debut)

if __name__ == "__main__":
    main()
