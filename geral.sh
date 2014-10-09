#!/usr/bin/env bash

xyrgb_arq=$1
# k do KNN Mutuo
k1=$2
# k do knn com rotulos
k2=$3
#
xyrgb_arq_name=$(basename $xyrgb_arq)
xyrgb_dir_name=$(dirname $xyrgb_arq)
labels_arq=$4
# arquivo com as distancias (distancias nao ordenada)
dist_arq=${xyrgb_dir_name}"/dist_"${xyrgb_arq_name}
# arquivo com indice dos knn mais proximos (ordenados por proximidade)
neig_arq=${xyrgb_dir_name}'/neig_'${xyrgb_arq_name}

# arquivo com o grafo criado
g_arq=${xyrgb_dir_name}"/graph_"${k1}"_"${k2}"_"${xyrgb_arq_name}

if [ ! -e $dist_arq ];
then
	python calc_dist.py $xyrgb_arq
fi

# numero de vertices
n=$(wc -l < $xyrgb_arq)

python lknn.py $n ${k1} $k2 $neig_arq $dist_arq $labels_arq $g_arq

cluster_arq=${xyrgb_dir_name}"/cluster_"${k1}"_"${k2}"_"${xyrgb_arq_name}

matlab -nojvm -nodisplay -nosplash -r "main('$g_arq','$cluster_arq',$n);quit()"