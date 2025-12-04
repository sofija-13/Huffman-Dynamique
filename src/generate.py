#! python3
# genere un fichier random<entier>.txt

import sys, random, string

def save(text, filename):
    """
    Écrit le texte généré dans un fichier filename
    
    Args:
        fichier (str): nom du fichier
        text (str): Texte à écrire
    """
    # filename : str = "texts/random"+str(n)+".txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Fichier aléatoire '{filename}' généré ({len(text)} caractères).")



def main():
    if len(sys.argv) < 2:
        print("Erreur generate: nombre d'arguments invalide.", file=sys.stderr)
        print("Usage: python generate.py <nom_fichier_souhaité>", file=sys.stderr)
        sys.exit(1)
    text = "texte"
    filename = sys.argv[1]
    save(text, filename)

if __name__ == "__main__":
    main()