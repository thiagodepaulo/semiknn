function [] = main(filename, k, resultname, n)
    file = importdata(filename);
    w = SparseMatrix(file, n);
    result = SpectralClustering(w,k,1);
    dlmwrite(resultname,result);
end
