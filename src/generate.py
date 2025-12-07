#! python3
# generate.py

import sys
import random
import string

def generate_text(length=13000, distribution=None):
    """
    Génère du texte aléatoire, multilingue, et avec emojis : 
    - latin avec lettres et diacritiques divers ajoutés (français, lituanien, espagnol et norvégien)
    - chinois simplifié (caractères courants) 
    - japonais (Hiragana et Katakana)
    - coréen 
    - cyrilique 
    - grec
    - quelques emojis 
    
    Args:
        length (int): Nombre de caractères à générer
        distribution (dict): Poids de chaque alphabet (optionnel)
            Ex: {'latin': 0.5, 'chinese': 0.3, 'emoji': 0.2}
            Si non spécifié, répartition égale entre tous les alphabets
    
    Returns:
        str: Texte aléatoire généré
    """
    
    # définition alphabets utilisés
    alphabets = {
        'latin': string.printable + 'ÉéÀàÈèÇçÙù' + 'ĄČĘĖĮŠŲŪŽąčęėįšųūž' + 'ÆæØøÅå' + 'ÁáÍíÓóÚú', 
                # ajout de lettres et diacritiques divers: français, lituanien, norvégien, espagnol
        
        # Chinois simplifié (caractères courants)
        'chinese': ''.join(chr(i) for i in range(0x4E00, 0x4E00 + 100)),
        
        # Japonais 
        'japanese': (
            ''.join(chr(i) for i in range(0x3040, 0x309F)) +  # Hiragana
            ''.join(chr(i) for i in range(0x30A0, 0x30FF))    # Katakana
        ),
        
        # Coréen (Hangul)
        'korean': ''.join(chr(i) for i in range(0xAC00, 0xAC00 + 100)),
        
        # Cyrillique (russe)
        'cyrillic': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        
        # grec
        'greek': 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω',
        
        # emojis 
        'emojis': '😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚☺️🙂🤗🤩🤔🤨😐😑😶🙄😏😣😥😮🤐😯😪😫🥱😴😌😛😜😝🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱🥵🥶😳🤪😵🥴😠😡🤬😷🤒🤕🤢🤮🤧😇🥳🥺🤠🤡🤥🤫🤭🧐🤓'
    }
    
    # Distribution par défaut : équitable entre tous les alphabets
    if distribution is None:
        num_alphabets = len(alphabets)
        distribution = {name: 1.0 / num_alphabets for name in alphabets.keys()}
    
    # Vérifier que tous les alphabets ont une distribution (même si 0)
    for alphabet_name in alphabets.keys():
        if alphabet_name not in distribution:
            distribution[alphabet_name] = 0.0
    
    # Normaliser la distribution pour qu'elle somme à 1.0
    total = sum(distribution.values())
    if total > 0:
        distribution = {k: v / total for k, v in distribution.items()}
    else:
        # Si toutes les valeurs sont à 0, répartition égale
        num_alphabets = len(alphabets)
        distribution = {name: 1.0 / num_alphabets for name in alphabets.keys()}
    
    # Construire l'alphabet combiné avec les poids
    combined_alphabet = []
    weights = []
    
    for alphabet_name, alphabet_chars in alphabets.items():
        alphabet_weight = distribution.get(alphabet_name, 0)
        
        if alphabet_weight > 0 and len(alphabet_chars) > 0:
            # Ajouter chaque caractère avec son poids proportionnel
            for char in alphabet_chars:
                combined_alphabet.append(char)
                weights.append(alphabet_weight / len(alphabet_chars))
    
    # Générer texte
    if not combined_alphabet:
        return ""
    
    return ''.join(random.choices(combined_alphabet, weights=weights, k=length))

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
    # Gérer arguments
    if len(sys.argv) < 2: 
        print("Erreur generate: nombre d'arguments invalide.", file=sys.stderr)
        print("Usage: python generate.py <nom_fichier_souhaité> [taille] [distribution]", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Gérer la taille (argument optionnel)
    length = 13000  # valeur par défaut
    if len(sys.argv) >= 3:
        try:
            length = int(sys.argv[2]) 
        except ValueError:
            print(f"Erreur: la taille '{sys.argv[2]}' n'est pas un nombre valide.", file=sys.stderr)
            sys.exit(1)
    
    # Gérer la distribution (argument optionnel)
    distribution = None
    if len(sys.argv) >= 4:
        try:
            # Format: "latin:0.7,emoji:0.2,chinese:0.1"
            pairs = sys.argv[3].split(',')
            distribution = {}
            for pair in pairs:
                alphabet, weight = pair.split(':')
                distribution[alphabet.strip()] = float(weight)
        except (ValueError, IndexError):
            print(f"Erreur: format de distribution invalide. Format attendu : 'alphabet:poids,alphabet:poids'", file=sys.stderr)
            print("Alphabets disponiables: latin, chinese, japanese, korean, cyrillic, greek, emojis", file=sys.stderr)
            sys.exit(1)
    
    # Générer le texte
    text = generate_text(length=length, distribution=distribution)
    
    # Sauvegarder
    save(text, filename)

if __name__ == "__main__":
    main()