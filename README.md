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

[Lien Rapport Overleaf](https://www.overleaf.com/7683873468ggjjjbbtmqwg#1bff2f) (actuellement en modification)

[Lien Diapo Canva](https://www.canva.com/design/DAG68VOx-co/xnu7T3NC2ZLkr3Se8pxgeg/edit?utm_content=DAG68VOx-co&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
---

TO DO:
À déposer dans une archive compressée (format zip ou tar.gz) sur moodle au plus tard le 16/12 à 23h59 :
- Rapport (au format pdf, d’une dizaine de pages)
- Code Source (avec vos jeux de données test)
- Transparents de présentation

- Optimisations possibles : tab des éléments insérés

---
### Tips : print un fichier en format binaire 
```bash
python3 -c "from bitarray import bitarray; ba = bitarray(); ba.fromfile(open('FILEPATH DU BINAIRE', 'rb')); print(ba.to01())"
```
##### Prérequis : bitarray installé
