function [] = main(filename, resultname, n)
    file = importdata(filename);
    w = SparseMatrix(file, n);
    result = SpectralClustering(w,15,1);
    dlmwrite(resultname,result);
end