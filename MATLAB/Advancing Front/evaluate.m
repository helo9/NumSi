function [ value ] = evaluate( P1, P2, P3array )
% Input P1 and P2 define the existing edge. P3 is the Point to evaluate. 
% Format Pi =[x,y] 
% function benefits small angle deviaions from 60° and small triangles
% weights the influence of bad angles
w1 = 2;

value = ones(size(P3array,1),1);
for i = 1:size(P3array,1)
    P3 = P3array(i,:);

c = P2 - P1;
a = P3 - P1;
b = P3 - P2;

normc = norm(c);
norma = norm(a);
normb = norm(b);

%v1 is small for small triangles v1 = O(1)
v1 = (norma+ normb)/(2*normc);

alpha = acos(  ( a     *c') /(norma*normc));
beta = acos(  ( b     *(-c)') /(normb*normc));
gamma = pi - alpha - beta;


%v2 is small for angles near 60° 0 <= v2 <= ^1
v2 =( ( abs(alpha - pi/3) + abs(beta - pi/3) + abs(gamma - pi/3) )/pi)^2;

value(i) = v1 + w1*v2^2;

end


end

