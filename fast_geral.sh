#!/usr/bin/env bash

usage() { echo "Usage: $0 -i <image file> -l <labels file> -c <number of clusters> -1 k1 -2 k2 [ -t <number of threads> ] " 1>&2; exit 1; }

image_arq=false
labels_arq=false
num_clusters=0
k1=false
k2=false
num_threads=2

while getopts 'i:l:c:1:2:t:' flag; do
  case "${flag}" in
    i) image_arq="${OPTARG}" ;;
    l) labels_arq="${OPTARG}" ;;
    c) num_clusters="${OPTARG}" ;;
    1) k1="${OPTARG}" ;;
    2) k2="${OPTARG}" ;;
    t) num_threads="${OPTARG}" ;;
    *) usage ;;
  esac
done


if [ ! -e $image_arq ]; then echo "Image File not found: $image_arq"; exit; fi
if [ ! -e $labels_arq ]; then echo "Labels File not found: $label_arq"; exit; fi
if [ $num_cluster = 0 ]; then echo "undefined number of clusters"; exit; fi

# arquivo com o grafo criado
labels_arq_name=$(basename $labels_arq)
labels_dir_name=$(dirname $labels_arq)
#g_arq=${labels_dir_name}"/graph_"${k1}"_"${k2}"_"${labels_arq_name}

echo "creating semisupervised graph..."
cluster_arq=${labels_dir_name}"/cluster_"${num_clusters}"_"${k1}"_"${k2}"_"${labels_arq_name}
python fast-knn-graph-construction.py -f $image_arq -1 $k1 -2 $k2 -l $labels_arq -o $cluster_arq -t $num_threads -c $num_clusters
echo "DONE: $cluster_arq"

#is_connected=$(python graph_is_connected.py $g_arq)
#if [ $is_connected == "False" ]; then echo "graph is not connected"; exit; fi

width=$(convert $image_arq -print "%w" /dev/null)	#dimension of x-axis
height=$(convert $image_arq -print "%h" /dev/null)	#dimension of x-axis

#n=$(($width * $height))		# number of pixels == number of vetices
# do spectral clustering -- matlab code!
#echo "doing spectral clustering...."
#cluster_arq=${labels_dir_name}"/cluster_"${num_clusters}"_"${k1}"_"${k2}"_"${labels_arq_name}
#matlab -nojvm -nodisplay -nosplash -r "main('$g_arq',$num_clusters,'$cluster_arq',$n); quit()"
#echo "DONE: $cluster_arq"

echo "re-creating segmented image"
python create_image.py -f $cluster_arq -x $width -y $height
echo "DONE: "

