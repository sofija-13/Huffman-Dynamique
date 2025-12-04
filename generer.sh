#!/usr/bin/env bash 

# crée des fichiers textuels et génère le texte aléatoirement 
# puis appelle le script pour les compresser 

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=${PYTHON_BIN:-python3}

output_dir="texts"

usage() {
  echo "Usage: ./generer.sh" "<nbre de fichiers souhaités>" 1>&2
  echo "Pour plus d'informations : ./generer.sh --help" 1>&2
  echo
}

if [[ $# -eq 0 ]]; then
  echo "Il manque un argument !" 1>&2
  usage
  exit 1
fi

if [[ ${1:-} == "--help" ]]; then
  usage
  echo Ce script crée N fichiers .txt dans le répertoire $output_dir et en génère le texte aléatoirement. 
  echo N doit être donné en paramètre
  exit 1
fi

# lancer le generateur de fichiers 

for (( i=0; i<$1; i++ )); do 
    # "$PYTHON_BIN" "$SCRIPT_DIR/generate.py" 
    echo sofija t'as oublié d'écrire le fichier generate.py sale conne
    exit 1
done

echo Fichiers générés dans "$output_dir"/
echo Compression...

# lancer compression des fichiers générés
# for fichier in "$output_dir/random*.txt" ; do 
#     "$SCRIPT_DIR/compresser" $fichier $($fichier | cut -d "." -f 1).huff
# done

