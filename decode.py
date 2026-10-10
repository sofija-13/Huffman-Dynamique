#! python3
import sys, bitarray, time, os
from src.utils import decode, writeStr, lecture

def infos_decompression(txt_path, bin_path, temps):
    txt_size = os.path.getsize(txt_path) if os.path.exists(txt_path) else 0
    bin_size = os.path.getsize(bin_path) if os.path.exists(bin_path) else 0
    taux_comp = bin_size / txt_size
    print(f"{bin_path};{txt_path};{txt_size};{bin_size};{taux_comp:.5f};{temps}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python decode.py <fichier_entree> <fichier_sortie>")
        sys.exit(1)
    elif (sys.argv[1]==sys.argv[2]):
        print("⚠️ Les fichiers d'entrée et sortie doivent être différents")
        sys.exit(1)
        
    contenu : bitarray = lecture(sys.argv[1])
    
    temps_debut = time.time()
    decoded = decode(contenu)
    temps_fin = time.time()
    writeStr(sys.argv[2], decoded)
    
    print(f"Fichier décodé avec succès: {sys.argv[1]} -> {sys.argv[2]}", file=sys.stderr)
    infos_decompression(sys.argv[1], sys.argv[2], (temps_fin-temps_debut)*1000)

if __name__ == "__main__":
    main()