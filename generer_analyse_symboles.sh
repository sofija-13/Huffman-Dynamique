#!/usr/bin/env bash

# Script pour générer des fichiers de taille fixe avec un nombre variable de symboles
# puis les compresser pour analyser l'impact du nombre de symboles sur la compression

OUTPUT_DIR="texts/analyse/symboles"
COMPRESSED_DIR="texts/bintexts"

# Créer les répertoires s'ils n'existent pas
mkdir -p "$OUTPUT_DIR"
mkdir -p "$COMPRESSED_DIR"

# Taille fixe des fichiers (en octets)
TAILLE_FIXE=10000

echo "=== Génération de fichiers avec nombre de symboles variable ==="
echo "Taille fixe: $TAILLE_FIXE octets"
echo ""

# Générer des fichiers avec différents nombres de symboles

# De 50 en 50 jusqu'à 1000
for nb_symboles in $(seq 50 50 1000); do
  filename="$OUTPUT_DIR/sym_${nb_symboles}.txt"
  echo "Génération: $filename ($nb_symboles symboles différents)"
  python3 "generer_fichier_utf8.py" \
    -t "$TAILLE_FIXE" \
    -s "$nb_symboles" \
    -o "$filename"
  echo ""
done

# De 500 en 500 au-dessus de 1000 jusqu'à 3000
for nb_symboles in $(seq 1500 500 3000); do
  filename="$OUTPUT_DIR/sym_${nb_symboles}.txt"
  echo "Génération: $filename ($nb_symboles symboles différents)"
  python3 "generer_fichier_utf8.py" \
    -t "$TAILLE_FIXE" \
    -s "$nb_symboles" \
    -o "$filename"
  echo ""
done

echo "=== Compression des fichiers générés ==="
echo ""

# Compresser tous les fichiers générés avec l'exécutable compresser
for file in "$OUTPUT_DIR"/sym_*.txt; do
  if [[ -f "$file" ]]; then
    basename=$(basename "$file" .txt)
    output_name="$COMPRESSED_DIR/${basename}.huff"
    echo "Compression: $OUTPUT_DIR/$basename.txt"
    
    # Utiliser l'exécutable compresser
    "./compresser" "$file" "$output_name"
    
    # Afficher les tailles pour comparaison
    if [[ -f "$output_name" ]]; then
      taille_originale=$(wc -c < "$file")
      taille_compresse=$(wc -c < "$output_name")
      ratio=$(echo "scale=2; $taille_compresse * 100 / $taille_originale" | bc)
      echo "  Original: $taille_originale octets | Compressé: $taille_compresse octets | Ratio: ${ratio}%"
    else
      echo "  Erreur: fichier compressé non créé"
    fi
    echo ""
  fi
done

echo "=== Terminé ==="
echo "Fichiers générés dans: texts/analyse/symboles"
echo "Fichiers compressés dans: texts/bintexts"