function PtIdxs = getTrianglePointIdx(Triangle)
    
    global Edge
    
    % Vektor für Punkt indizes
    PtIdxs = [];
    
    for ii = 1:3
        EdgeIdx = Triangle(ii);
        for jj = 1:2
            if isempty(find(PtIdxs == Edge(EdgeIdx,jj)))
                PtIdxs(end+1) = Edge(EdgeIdx,jj);
            end %if
        end %for
    end %while
end %function
            