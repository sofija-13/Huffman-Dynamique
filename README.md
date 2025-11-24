#### UM4IN500
# Projet Huffman Dynamique
Projet d'Algorithmique Avancée (ALGAV) du M1 Informatique de Sorbonne Université

Langage utilisé : **Python 3** - Version 1.14, dernière version  (Octobre 2025)

---
### Installation
#### Création d'un venv Python
```bash
python -m venv env
source env/bin/activate 
```
#### Installation du module *bitarray*
```bash
pip3 install bitarray
```
---

[Lien Rapport Overleaf](https://www.overleaf.com/7683873468ggjjjbbtmqwg#1bff2f) (actuellement en modification)

---

TO DO:

- "Veillez à indiquer dans le README de votre projet, le langage que vous avez utilisé, sa version et le compilateur utilisé ainsi que sa version."

À déposer dans une archive compressée (format zip ou tar.gz) sur moodle au plus tard le 16/12 à 23h59 :
- Rapport (au format pdf, d’une dizaine de pages)
- Code Source (avec vos jeux de données test)
- Transparents de présentation

---
### Tips : print un fichier en format binaire 
```bash
python3 -c "from bitarray import bitarray; ba = bitarray(); ba.fromfile(open('FILEPATH DU BINAIRE', 'rb')); print(ba.to01())"
```
##### Prérequis : bitarray installé