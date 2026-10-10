#### UM4IN500
# Projet Huffman dynamique

Projet d'Algorithmique Avancee (ALGAV) du M1 Informatique de Sorbonne Universite.

Ce projet implemente une compression et une décompression par **algorithme de Huffman adaptatif**. L'arbre de Huffman est construit et mis a jour pendant la lecture du texte : il n'est donc pas nécessaire de construire un arbre statique a partir d'une table de frequences avant l'encodage.

## Fonctionnalites

- compression d'un fichier texte en un fichier binaire `.huff` ;
- decompression d'un fichier `.huff` vers un fichier texte ;
- mise a jour dynamique des poids et de la structure de l'arbre ;
- mesure du temps d'exécution et du taux de compression ;
- jeux de donnees et notebooks pour analyser l'influence de la longueur et du nombre de symboles.

Le symbole NYT (Not Yet Transmitted) permet de transmettre un nouveau caractère la première fois qu'il apparait. Les symboles sont manipulés comme des caractères Unicode et les nouveaux caractères sont stockes en UTF-8.

## Installation

Le projet utilise Python 3 et le module `bitarray` pour manipuler les flux de bits. Les notebooks d'analyse utilisent également `pandas`, `matplotlib` et `numpy`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install bitarray pandas matplotlib numpy
```

## Utilisation

Les scripts shell peuvent être lancés depuis la racine du projet.

### Compression

```bash
./compresser fichier_entree.txt fichier_sortie.huff
```

Exemple :

```bash
./compresser texts/Blaise_Pascal/Blaise_Pascal.txt /tmp/pascal.huff
```

Le script appelle `encode.py` et enregistre les statistiques dans `compression.txt`.

### Décompression

```bash
./decompresser fichier_entree.huff fichier_sortie.txt
```

Exemple :

```bash
./decompresser /tmp/pascal.huff /tmp/pascal-restaure.txt
```

Les fichiers d'entrée et de sortie doivent être différents. Les scripts Python peuvent aussi être appelés directement :

```bash
python3 encode.py fichier_entree.txt fichier_sortie.huff
python3 decode.py fichier_entree.huff fichier_sortie.txt
```

## Organisation du projet

```text
.
├── compresser                 # Lanceur shell de compression
├── decompresser               # Lanceur shell de decompression
├── encode.py                  # Entree de l'encodage fichier
├── decode.py                  # Entree du decodage fichier
├── src/
│   ├── Node.py                # Noeuds et parcours de l'arbre
│   ├── utils.py               # Encodage, decodage et I/O binaire
│   └── generate.py            # Generation de donnees de test
├── texts/                     # Textes d'exemple et resultats
├── tests/                     # Donnees, scripts et notebooks d'analyse
├── demo/                      # Demonstrations et notebooks
└── resources/                 # Documentation complementaire
```

## Tests et analyses

Les scripts du dossier `tests/` servent a générer des jeux de données pour les analyses de longueur et de nombre de symboles :

```bash
./tests/generer.sh
./tests/generer_analyse_len.sh
./tests/generer_analyse_symboles.sh
```

Les fichiers `tests/analyse.ipynb`, `tests/tests.ipynb` et `demo/` peuvent être ouverts avec Jupyter ou VS Code.

Pour afficher les bits d'un fichier binaire :

```bash
python3 -c "from bitarray import bitarray; bits = bitarray(); bits.fromfile(open('fichier.huff', 'rb')); print(bits.to01())"
```

