#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer des fichiers UTF-8 de taille spécifique
avec un nombre contrôlé de symboles différents.
"""

import argparse
import random
import os


def generer_fichier_utf8(taille_cible, nombre_symboles, fichier_sortie):
    """
    Génère un fichier UTF-8 de taille approximative spécifiée.
    
    Args:
        taille_cible: Taille cible du fichier en octets
        nombre_symboles: Nombre de symboles différents à utiliser
        fichier_sortie: Chemin du fichier de sortie
    """
    if nombre_symboles < 1:
        raise ValueError("Le nombre de symboles doit être au moins 1")
    
    # Pool de symboles disponibles (caractères UTF-8 variés)
    # Inclut des caractères ASCII, latins étendus, grecs, cyrilliques, chinois, etc.
    # Génération dynamique de pools étendus à partir de plages Unicode
    pools = []
    
    # ASCII imprimables 
    pools.append('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n.,;:!?-\'\"()[]{}@#$%&*+=/<>\\|`~_')
    
    # Latin étendu (U+0100 à U+017F)
    pools.append(''.join(chr(i) for i in range(0x0100, 0x0180) if chr(i).isprintable()))
    
    # Latin supplémentaire (U+0180 à U+024F)
    pools.append(''.join(chr(i) for i in range(0x0180, 0x0250) if chr(i).isprintable()))
    
    # IPA Extensions (U+0250 à U+02AF)
    pools.append(''.join(chr(i) for i in range(0x0250, 0x02B0) if chr(i).isprintable()))
    
    # Espacement combinant (U+02B0 à U+02FF)
    pools.append(''.join(chr(i) for i in range(0x02B0, 0x0300) if chr(i).isprintable()))
    
    # Grec (U+0370 à U+03FF)
    pools.append(''.join(chr(i) for i in range(0x0370, 0x0400) if chr(i).isprintable()))
    
    # Cyrillique (U+0400 à U+04FF)
    pools.append(''.join(chr(i) for i in range(0x0400, 0x0500) if chr(i).isprintable()))
    
    # Arabe (U+0600 à U+06FF)
    pools.append(''.join(chr(i) for i in range(0x0600, 0x0700) if chr(i).isprintable()))
    
    # Hébreu (U+0590 à U+05FF)
    pools.append(''.join(chr(i) for i in range(0x0590, 0x0600) if chr(i).isprintable()))
    
    # Thaï (U+0E00 à U+0E7F)
    pools.append(''.join(chr(i) for i in range(0x0E00, 0x0E80) if chr(i).isprintable()))
    
    # Lao (U+0E80 à U+0EFF)
    pools.append(''.join(chr(i) for i in range(0x0E80, 0x0F00) if chr(i).isprintable()))
    
    # Géorgien (U+10A0 à U+10FF)
    pools.append(''.join(chr(i) for i in range(0x10A0, 0x1100) if chr(i).isprintable()))
    
    # Jamo hangul (U+1100 à U+11FF)
    pools.append(''.join(chr(i) for i in range(0x1100, 0x1200) if chr(i).isprintable()))
    
    # Syllables hangul (U+AC00 à U+D7AF)
    pools.append(''.join(chr(i) for i in range(0xAC00, 0xD7B0, 100) if chr(i).isprintable()))  # Échantillonné pour performance
    
    # Hiragana (U+3040 à U+309F)
    pools.append(''.join(chr(i) for i in range(0x3040, 0x30A0) if chr(i).isprintable()))
    
    # Katakana (U+30A0 à U+30FF)
    pools.append(''.join(chr(i) for i in range(0x30A0, 0x3100) if chr(i).isprintable()))
    
    # Caractères idéographiques CJK (U+4E00 à U+9FFF) - Échantillonnés
    pools.append(''.join(chr(i) for i in range(0x4E00, 0x9FF0, 50) if chr(i).isprintable()))
    
    # Symboles mathématiques (U+2200 à U+22FF)
    pools.append(''.join(chr(i) for i in range(0x2200, 0x2300) if chr(i).isprintable()))
    
    # Opérateurs mathématiques (U+2190 à U+21FF)
    pools.append(''.join(chr(i) for i in range(0x2190, 0x2200) if chr(i).isprintable()))
    
    # Formes géométriques (U+25A0 à U+25FF)
    pools.append(''.join(chr(i) for i in range(0x25A0, 0x2600) if chr(i).isprintable()))
    
    # Symboles divers (U+2600 à U+26FF)
    pools.append(''.join(chr(i) for i in range(0x2600, 0x2700) if chr(i).isprintable()))
    
    # Tiret (U+2700 à U+27BF)
    pools.append(''.join(chr(i) for i in range(0x2700, 0x27C0) if chr(i).isprintable()))
    
    # Formes mathématiques alphanumériques (U+1D400 à U+1D7FF)
    pools.append(''.join(chr(i) for i in range(0x1D400, 0x1D800, 2) if chr(i).isprintable()))
    
    # Flèches supplémentaires (U+27F0 à U+27FF)
    pools.append(''.join(chr(i) for i in range(0x27F0, 0x2800) if chr(i).isprintable()))
    
    # Créer un pool combiné de tous les caractères disponibles (en éliminant les doublons)
    tous_symboles_set = set(''.join(pools))
    tous_symboles = list(tous_symboles_set)
    
    print(f"Pool total de symboles uniques disponibles: {len(tous_symboles)}")
    
    # Sélectionner le nombre de symboles demandé
    if nombre_symboles > len(tous_symboles):
        print(f"Attention: nombre de symboles demandé ({nombre_symboles}) > disponibles ({len(tous_symboles)})")
        print(f"Utilisation de tous les symboles disponibles: {len(tous_symboles)}")
        symboles_liste = tous_symboles
    else:
        # Sélection aléatoire de symboles uniques
        symboles_liste = random.sample(tous_symboles, nombre_symboles)
    
    symboles = ''.join(symboles_liste)
    
    print(f"Génération avec {len(symboles)} symboles différents")
    print(f"Échantillon: {symboles[:50]}{'...' if len(symboles) > 50 else ''}")
    
    # Générer le contenu
    contenu = []
    taille_actuelle = 0
    
    # D'abord, garantir que chaque symbole apparaît au moins une fois
    contenu = list(symboles)
    taille_actuelle = len(''.join(contenu).encode('utf-8'))
    
    # Ensuite, remplir jusqu'à atteindre la taille cible
    while taille_actuelle < taille_cible:
        # Choisir un symbole aléatoire
        symbole = random.choice(symboles)
        contenu.append(symbole)
        
        # Calculer la taille en octets UTF-8
        taille_actuelle = len(''.join(contenu).encode('utf-8'))
    
    # Écrire le fichier
    texte_final = ''.join(contenu)
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        f.write(texte_final)
    
    # Vérifier la taille réelle
    taille_reelle = os.path.getsize(fichier_sortie)
    print(f"Fichier généré: {fichier_sortie}")
    print(f"Taille cible: {taille_cible} octets")
    print(f"Taille réelle: {taille_reelle} octets")
    print(f"Nombre de caractères: {len(texte_final)}")
    
    # Vérifier le nombre de symboles uniques réellement utilisés
    symboles_uniques = len(set(texte_final))
    print(f"Symboles uniques dans le fichier: {symboles_uniques}")


def main():
    parser = argparse.ArgumentParser(
        description='Génère un fichier UTF-8 de taille spécifique avec un nombre contrôlé de symboles différents.'
    )
    parser.add_argument(
        '-t', '--taille',
        type=int,
        default=10000,
        help='Taille cible du fichier en octets (défaut: 10000)'
    )
    parser.add_argument(
        '-s', '--symboles',
        type=int,
        default=50,
        help='Nombre de symboles différents à utiliser (défaut: 50)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='fichier_genere.txt',
        help='Nom du fichier de sortie (défaut: fichier_genere.txt)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Seed pour le générateur aléatoire (pour la reproductibilité)'
    )
    
    args = parser.parse_args()
    
    # Initialiser le générateur aléatoire
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Seed aléatoire: {args.seed}")
    
    # Générer le fichier
    generer_fichier_utf8(args.taille, args.symboles, args.output)


if __name__ == '__main__':
    main()



"""
# Générer un fichier de 10000 octets avec 50 symboles différents
python3 generer_fichier_utf8.py

# Générer un fichier de 20000 octets avec 100 symboles
python3 generer_fichier_utf8.py -t 20000 -s 100 -o mon_fichier.txt

# Avec seulement 10 symboles différents
python3 generer_fichier_utf8.py -t 10000 -s 10 -o simple.txt

# Générer avec seed pour reproductibilité
python3 generer_fichier_utf8.py -t 10000 -s 30 --seed 42
"""