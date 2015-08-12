
for (( k=10; k<=500; k=k+10 )); do 
	echo "rodando para $k"; 
	./geral_knn.sh -i ../label_propag_testes/EstrelaDoMar.jpg -l ../label_propag_testes/strela.ui2.labels -c 12 -1 $k -t 8; 
done

for (( k=10; k<=500; k=k+10 )); do 
        echo "rodando para $k"; 
        ./geral_knn.sh -i ../label_propag_testes/Flor.jpg -l ../label_propag_testes/flor.ui1.labels -c 13 -1 $k -t 8;
done

