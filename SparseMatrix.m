function [M] = SparseMatrix(EdgeList,n)

    edges = size(EdgeList,1);
    M = sparse(n,n);
    for i=1:edges
        v = EdgeList(i,1)+1;
        u = EdgeList(i,2)+1;
        w = EdgeList(i,3);
        M(v,u) = w;
        M(u,v) = w;
    end
    
end