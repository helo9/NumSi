function [ Point, radius ] = getcircumcircle( P1, P2, P3 )

%Berechnung der Seitenlängen

a = getveclength(P1,P2);
b = getveclength(P2,P3);
c = getveclength(P1,P3);
A = P1 - P2;
B = P2 - P3;
A3 = [A 0];
B3 = [B 0];

f = norm(cross(A3,B3))*1/2;

radius = a*b*c/(f*4);
NA = [-A(2) A(1)];
NB = [-B(2) B(1)];

Nmat = [NB(1) -NA(1); NB(2) -NA(2)];

bb = (P2 + 0.5 * A - (0.5 *B + P3))';
st = Nmat\bb;
st = st';

Point = P2 + 0.5*A + st(2)*NA;











        %Subfunktionen
    function [length] = getveclength(P1,P2)
        length =  sqrt((P1(1)-P2(1))^2 + (P1(2) - P2(2))^2);
    end


end

