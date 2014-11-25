% Ränder definieren

north = [0,5;1.5,5;2,5;4,5;5,5;10,5];
east  = [10,1;10,2;10,3;10,5];
south = [0,0;1,0;7,0;8,1;9,1;10,1];
west  = [0,0;0,1;0,2.5;0,5];

%north = [0,5;5,5;8,5;10,5];
%east  = [10,0;9,2.5;10,5];
%south = [0,0;5,0;8,1;10,0];
%west  = [0,0;1,2.5;0,5];

figure(1)
clf;
hold on;

M = size(north,1)-1;
N = size(east,1)-1;

xs = @(xi) south(xi+1,:);
xn = @(xi) north(xi+1,:);
xw = @(eta)west(eta+1,:);
xe = @(eta)east(eta+1,:);

ptsx = ptsy = zeros(M+1,N+1);

% logisches Gitter durch iterieren
for xi = [0:M]
    
    cp = zeros(M+1,2);
    
    for eta = [0:N]
        % Interpolationsvorschrift S. 59
        pt = (1-eta/M)*xs(xi)+(eta/M)*xn(xi)+(1-xi/N)*xw(eta)+xi/N*xe(eta)...
            - xi/N*(eta/M*xn(M)+(1-eta/M)*xs(M))-(1-xi/N)*(eta/M*xn(0)+(1-eta/M)*xs(0));
        ptsx(xi+1,eta+1) = pt(1);
        ptsy(xi+1,eta+1) = pt(2);
        plot(pt(1),pt(2),'r+');
        % Punkte plotten
        disp([num2str([xi,eta]),'-',num2str(pt)])
        % Kanten plotten
        if(xi>0)
            % horizontale Linien plotten
            plot([ptsx(xi,eta+1),pt(1)],[ptsy(xi,eta+1),pt(2)],'b-')
        end %if
        if(eta>0)
            % vertikale Linien plotten
            plot([ptsx(xi+1,eta),pt(1)],[ptsy(xi+1,eta),pt(2)],'g-')
        end %if
    end %for
end %for