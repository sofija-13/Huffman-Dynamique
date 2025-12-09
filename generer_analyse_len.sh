for size in $(seq 1000 1000 100000); do
  base="analyse/len_$((size/10))"   # donne len_1000 -> fichier len_10000.txt, etc.
  ./generer.sh 1 "$base" "$size" "latin:1"
done