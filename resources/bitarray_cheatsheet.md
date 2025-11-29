# Cheatsheet Bitarray Python 🔧

Guide complet de la bibliothèque `bitarray` pour la manipulation de données binaires.

---

## 📦 Installation

```bash
pip install bitarray
```

```python
from bitarray import bitarray
```

---

## 🆕 Création d'un bitarray

### À partir de zéro
```python
ba = bitarray()              # Bitarray vide
ba = bitarray(10)            # 10 bits non initialisés
ba = bitarray(10, endian='big')  # Avec ordre des bits spécifié
```

### À partir d'une string binaire
```python
ba = bitarray('10110101')    # String de 0 et 1
```

### À partir d'une liste/itérable
```python
ba = bitarray([1, 0, 1, 1])  # Liste de 0 et 1
ba = bitarray([True, False, True])  # Liste de booléens
```

### À partir de bytes
```python
ba = bitarray()
ba.frombytes(b'hello')       # Depuis des bytes
```

### À partir d'un entier
```python
ba = bitarray()
ba.frombytes((42).to_bytes(1, 'big'))  # Convertir entier → bytes → bitarray
```

---

## 📖 Lecture de fichiers

### Lire un fichier binaire
```python
ba = bitarray()
with open('fichier.bin', 'rb') as f:
    ba.fromfile(f)
```

### Lire un fichier texte UTF-8
```python
ba = bitarray()
with open('fichier.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    ba.frombytes(text.encode('utf-8'))
```

---

## 💾 Écriture dans des fichiers

### Écrire dans un fichier binaire
```python
with open('output.bin', 'wb') as f:
    ba.tofile(f)
```

---

## 🔄 Conversions

### Bitarray → String binaire
```python
binary_string = ba.to01()    # '10110101'
```

### Bitarray → Bytes
```python
data = ba.tobytes()          # b'\xb5' (padding automatique)
```

### Bitarray → Liste
```python
liste = ba.tolist()          # [1, 0, 1, 1, 0, 1, 0, 1]
```

### Bitarray → Entier
```python
# Méthode 1 : Via bytes
nombre = int.from_bytes(ba.tobytes(), 'big')

# Méthode 2 : Via string binaire
nombre = int(ba.to01(), 2)
```

### Bitarray → Texte UTF-8
```python
texte = ba.tobytes().decode('utf-8')
```

---

## ✂️ Manipulation de base

### Accès aux éléments
```python
ba[0]                        # Premier bit (True ou False)
ba[-1]                       # Dernier bit
ba[2:5]                      # Slice : bitarray('101')
ba[::2]                      # Tous les 2 bits
```

### Modification
```python
ba[0] = 1                    # Modifier un bit
ba[0] = True                 # Équivalent
ba[2:5] = bitarray('110')    # Modifier une plage
```

### Longueur
```python
len(ba)                      # Nombre de bits
```

---

## ➕ Ajout et extension

```python
ba.append(1)                 # Ajouter un bit à la fin
ba.append(True)              # Équivalent

ba.extend([0, 1, 1])         # Ajouter plusieurs bits
ba.extend(bitarray('0110'))  # Ajouter un autre bitarray

ba.insert(2, 1)              # Insérer un bit à l'index 2
```

---

## ❌ Suppression

```python
ba.pop()                     # Supprimer et retourner le dernier bit
ba.pop(3)                    # Supprimer et retourner le bit à l'index 3

ba.remove(1)                 # Supprimer la première occurrence de 1

del ba[2]                    # Supprimer le bit à l'index 2
del ba[2:5]                  # Supprimer une plage

ba.clear()                   # Vider le bitarray
```

---

## 🔍 Recherche

```python
ba.count()                   # Nombre de bits à 1
ba.count(0)                  # Nombre de bits à 0

ba.index(1)                  # Index du premier 1
ba.index(1, start, stop)     # Recherche dans une plage

1 in ba                      # Vérifier si 1 est présent
ba.any()                     # True si au moins un bit à 1
ba.all()                     # True si tous les bits à 1
```

---

## 🔀 Opérations bit-à-bit

### Opérations logiques (in-place)
```python
ba1 = bitarray('1010')
ba2 = bitarray('1100')

ba1 &= ba2                   # AND in-place : '1000'
ba1 |= ba2                   # OR in-place  : '1110'
ba1 ^= ba2                   # XOR in-place : '0110'
ba1.invert()                 # NOT in-place : inverse tous les bits
```

### Opérations logiques (créent un nouveau bitarray)
```python
ba3 = ba1 & ba2              # AND
ba3 = ba1 | ba2              # OR
ba3 = ba1 ^ ba2              # XOR
ba3 = ~ba1                   # NOT (inversion)
```

---

## 🔄 Décalages et rotations

```python
ba = bitarray('10110')

# Décalages (shift)
ba << 2                      # Décalage gauche : '11000'
ba >> 2                      # Décalage droite : '00101'

# Pas de rotation native, mais on peut faire :
def rotate_left(ba, n):
    n = n % len(ba)
    return ba[n:] + ba[:n]

def rotate_right(ba, n):
    n = n % len(ba)
    return ba[-n:] + ba[:-n]
```

---

## 🔁 Copie et comparaison

```python
ba2 = ba.copy()              # Copie profonde
ba2 = ba[:]                  # Aussi une copie

ba1 == ba2                   # Comparaison
ba1 != ba2
ba1 < ba2                    # Comparaison lexicographique
```

---

## 🔧 Autres opérations utiles

### Inversion
```python
ba.invert()                  # Inverse tous les bits (in-place)
ba.invert(3, 7)              # Inverse les bits de l'index 3 à 6
```

### Remplissage (fill)
```python
ba.fill()                    # Remplit le dernier octet avec des 0
```

### Setall
```python
ba.setall(0)                 # Met tous les bits à 0
ba.setall(1)                 # Met tous les bits à 1
```

### Reverse
```python
ba.reverse()                 # Inverse l'ordre des bits
```

### Sort
```python
ba.sort()                    # Trie les bits (met les 0 avant les 1)
ba.sort(reverse=True)        # Trie en ordre inverse
```

---

## 📊 Informations sur le bitarray

```python
len(ba)                      # Nombre de bits
ba.buffer_info()             # Infos mémoire (adresse, taille, etc.)
ba.endian()                  # Ordre des bits : 'big' ou 'little'
```

---

## 🎯 Cas d'usage : Huffman

### Encoder un caractère en bits
```python
code = bitarray('1011')      # Code Huffman pour un caractère
encoded = bitarray()
encoded.extend(code)
```

### Lire bit par bit
```python
for bit in ba:
    print(bit)               # True ou False
```

### Découper en octets
```python
def cut_bytes(ba):
    result = []
    for i in range(0, len(ba), 8):
        result.append(ba[i:i+8])
    return result
```

### Sauvegarder l'arbre compressé
```python
# Encoder
compressed = bitarray()
compressed.extend(bitarray('1011'))  # Ajouter codes Huffman

# Sauvegarder
with open('compressed.huf', 'wb') as f:
    compressed.tofile(f)

# Charger
decompressed = bitarray()
with open('compressed.huf', 'rb') as f:
    decompressed.fromfile(f)
```

---

## ⚡ Performance Tips

1. **Utiliser `extend()` plutôt que des `append()` multiples**
   ```python
   # ❌ Lent
   for bit in bits:
       ba.append(bit)
   
   # ✅ Rapide
   ba.extend(bits)
   ```

2. **Préallouer la taille si connue**
   ```python
   ba = bitarray(1000)  # Préallocation
   ```

3. **Utiliser `frombytes()` et `tobytes()` pour les conversions**
   ```python
   # ✅ Rapide (implémenté en C)
   ba.frombytes(data)
   ```

---

## 🔗 Ressources

- Documentation officielle : https://pypi.org/project/bitarray/
- GitHub : https://github.com/ilanschnell/bitarray

---

## 📝 Exemple complet : Compression simple

```python
from bitarray import bitarray

# Lire un fichier texte
ba = bitarray()
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    ba.frombytes(text.encode('utf-8'))

print(f"Nombre de bits: {len(ba)}")
print(f"Premiers 50 bits: {ba[:50].to01()}")

# Compresser (exemple simplifié)
compressed = bitarray()
for i in range(0, len(ba), 2):
    if i+1 < len(ba):
        compressed.append(ba[i] ^ ba[i+1])  # XOR de paires

# Sauvegarder
with open('output.bin', 'wb') as f:
    compressed.tofile(f)

print(f"Taux de compression: {len(compressed)/len(ba)*100:.2f}%")
```

---

## 🎓 Résumé rapide

| Opération | Syntaxe |
|-----------|---------|
| Créer | `bitarray('1011')` |
| Lire fichier | `ba.fromfile(f)` |
| Écrire fichier | `ba.tofile(f)` |
| → String | `ba.to01()` |
| → Bytes | `ba.tobytes()` |
| Ajouter | `ba.append(1)` / `ba.extend([0,1])` |
| Longueur | `len(ba)` |
| AND/OR/XOR | `ba1 & ba2` / `ba1 \| ba2` / `ba1 ^ ba2` |
| Inverser | `~ba` ou `ba.invert()` |
| Compter 1s | `ba.count()` |

---

**Bon codage avec bitarray! 🚀**
