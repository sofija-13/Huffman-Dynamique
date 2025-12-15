#### UM4IN500
# Projet Huffman Dynamique
Projet d'Algorithmique Avancée (ALGAV) du M1 Informatique de Sorbonne Université

Langage utilisé : **Python 3** - Version 1.14, dernière version  (Octobre 2025)

---
### Installation
#### Création d'un venv Python
```bash
python3 -m venv .venv
source .venv/bin/activate 
```
#### Installation des modules nécessaires : *bitarray*, *pandas*, *matplotlib*, *numpy*
```bash
pip3 install bitarray pandas matplotlib numpy
```

---

### Tips : print un fichier en format binaire 
```bash
python3 -c "from bitarray import bitarray; ba = bitarray(); ba.fromfile(open('FILEPATH DU BINAIRE', 'rb')); print(ba.to01())"
```
##### Prérequis : bitarray installé
