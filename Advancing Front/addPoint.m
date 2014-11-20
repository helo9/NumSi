function pid = addPoint(x,y)
    global Point
    
    Point(end+1) = [x,y]
    
    pid = length(Point)
    
end %function