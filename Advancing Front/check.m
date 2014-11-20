function [ legal ] = check( P1, P2, P3, NewPoint )
%Input P1 and P2 define the existing edge. P3 is the Point to evaluate.
% Format Pi =[x,y]
%   checks if a Point in Point or NewPoint is inside the new triangle and
%   if an existing edge crosses the triangle.
%   returns 1 if the triangle is legal 0 if it isnt

global Edge Point

legal = 1;
c = P2 - P1;
a = P3 - P1;
b = P3 - P2;


%case a: Point inside the triangle

Pointges = [Point; NewPoint];

for i = 1:size(Pointges,1);
    actpoint = Pointges(i,:);
    if isequal(P1,actpoint) || isequal(P2,actpoint) || isequal(P3,actpoint)
        continue;
    end
    b1 = (actpoint - P1)';
    mat1 = [c(1) a(1);c(2) a(2)];

    t1r1 = mat1\b1;

    b2 = (actpoint - P3)';
    mat2 = [-b(1) -a(1);-b(2) -a(2)];

    s2r2 = mat2\b2;
    
    if t1r1(1) < 0 || t1r1(2) < 0 || s2r2(1) < 0 || s2r2(2) < 0 || t1r1(1) > 1 || t1r1(2) > 1 || s2r2(1) > 1 || s2r2(2) > 1
    else
        legal = 0; 
        return;
    end
 
end

% case b edge cutting triangle --> P3P1 cutted by edge;

for  i = 1:size(Edge,1)
    actedge = Edge(i,:);
    if isequal(Point(actedge(1),:), P1) && isequal(Point(actedge(2),:), P2) || (isequal(Point(actedge(1),:), P2) && isequal(Point(actedge(2),:), P1));
        continue;
    end
    P1e = Point(actedge(1),:);
    P2e = Point(actedge(2),:);
    ve = P2e -P1e;
    
    be = (P1-P1e)';
    mate = [-a(1) ve(1);-a(2) ve(2)];
    
    rs = mate\be;
    
    if isnan(rs(1))
        continue;  
    end
    
    if rs(1) < 1 && rs(1) > 0 && rs(2) < 1 && rs(2) > 0
        legal = 0;
        return;
    end
    
    
end


end

