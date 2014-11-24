function [ Pidx ] = getPointidx( P )

global Point
for i = 1:size(Point,1)
    if  P == Point(i,:)
        Pidx = i;
        return;
    end
end
%not found
Pidx = -1;
return;

end

