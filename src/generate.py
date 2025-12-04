#! python3
# genere un fichier random<entier>.txt

import sys
import random
import string

def generate_text(length=13000):
    #definir alphabet qu'on utilise 
    alphabet = string.printable
    res : str = ''
    return res.join(random.choices(alphabet, k=length))


def save(text, filename):
    """
    Écrit le texte généré dans un fichier filename
    
    Args:
        fichier (str): nom du fichier
        text (str): Texte à écrire
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Fichier aléatoire '{filename}' généré ({len(text)} caractères).")



def main():
    # gerer arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3: 
        print("Erreur generate: nombre d'arguments invalide.", file=sys.stderr)
        print("Usage: python generate.py <nom_fichier_souhaité>", file=sys.stderr)
        sys.exit(1)
    text = ""
    if len(sys.argv) == 3 :
        text = generate_text(length=sys.argv[2]) 
    else :
        text = generate_text()
    filename = sys.argv[1]
    save(text, filename)

if __name__ == "__main__":
    main()