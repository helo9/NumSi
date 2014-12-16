function deleteEdge(Index)
    
    global Edge Triangle
    
    Edge(Index,:) = [];
    
    Triangle = Triangle - (Triangle > Index);
end % function