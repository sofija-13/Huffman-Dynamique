#!/usr/bin/env bash 

# Crée des fichiers textuels avec texte aléatoire multilingue
# puis appelle le script pour les compresser 

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=${PYTHON_BIN:-python3}
PROJECT_DIR="$(dirname "$SCRIPT_DIR")" #Huffman-Dynamique

output_dir=$PROJECT_DIR"/texts/random"
compressed_dir=$PROJECT_DIR"/texts/random/bintexts"

usage() {
  echo "Usage: ./generer.sh <nombre_fichiers> <base_nom> [taille] [distribution]" 1>&2
}

help_message() {
  usage
  echo "Ce script crée N fichiers .txt dans le répertoire $output_dir et génère leur contenu aléatoirement."
  echo
  echo "Arguments:"
  echo "  nombre_fichiers : Nombre de fichiers à générer (obligatoire)"
  echo "  base_nom        : Base des noms de fichier (obligatoire, exemple : random -> random0.txt, random1.txt, etc)"
  echo "  taille          : Nombre de caractères par fichier (optionnel, défaut: 13000)"
  echo "  distribution    : Répartition des alphabets (optionnel, format: 'latin:0.7,emojis:0.3')"
  echo
  echo "Alphabets disponibles:"
  echo "  latin    chinese    japanese    korean    cyrillic    greek    emojis"
  echo
  echo "Exemples:"
  echo "  ./generer.sh 10 random                                # 10 fichiers random0...9.txt de 13000 caractères"
  echo "  ./generer.sh 5 test 5000                              # 5 fichiers test0...4.txt de 5000 caractères"
  echo "  ./generer.sh 3 data 10000 'latin:0.7,emojis:0.2'      # 3 fichiers personnalisés data0...2.txt"
  echo
  exit 0
}
if [[ ${1:-} == "--help" ]]; then
  help_message
fi

if [[ $# -lt 2 ]]; then
  echo "Erreur: Il manque des arguments obligatoires !" 1>&2
  usage
  echo "Pour plus d'informations : ./generer.sh --help" 1>&2
  echo
  exit 1
fi

# Vérifier que le premier argument est un nombre
if ! [[ $1 =~ ^[0-9]+$ ]]; then
  echo "Erreur: Le nombre de fichiers doit être un entier positif." 1>&2
  usage
  exit 1
fi

num_files=$1
base_name=$2
file_size=${3:-}  # optionnel
distribution=${4:-}  # optionnel

# Créer les répertoires si nécessaire
mkdir -p "$output_dir"
mkdir -p "$compressed_dir"

echo "================================="
echo "GÉNÉRATION DES FICHIERS"
echo "================================="
echo "Nombre de fichiers : $num_files"
echo "Base des noms      : ${base_name}"
[[ -n $file_size ]] && echo "Taille par fichier : $file_size caractères"
[[ -n $distribution ]] && echo "Distribution       : $distribution"
echo

# Générer les fichiers
for (( i=0; i<$num_files; i++ )); do
    filename="$output_dir/${base_name}${i}.txt"
    
    # Construire la commande avec arguments optionnels
    cmd=("$PYTHON_BIN" "$PROJECT_DIR/src/generate.py" "$filename")
    [[ -n $file_size ]] && cmd+=("$file_size")
    [[ -n $distribution ]] && cmd+=("$distribution")
    
    "${cmd[@]}" &
done
wait

echo
echo "$num_files fichiers générés dans $output_dir"
echo

# Lancer compression des fichiers générés
if [[ -x $PROJECT_DIR"/compresser" ]]; then
    echo "========================"
    echo "COMPRESSION DES FICHIERS"
    echo "========================"
    
    cd "$output_dir" || exit 1
    
    for fichier in "${base_name}"*.txt; do
        if [[ -f $fichier ]]; then
            output_name="./bintexts/$(basename "$fichier" .txt).huff"
            $PROJECT_DIR/compresser "$fichier" "$output_name" 
        fi
    done
            
    echo
    echo "Tous les fichiers ont été compressés dans $compressed_dir"
else
    echo "Script 'compresser' introuvable ou non exécutable. Compression ignorée." 1>&2
fi
