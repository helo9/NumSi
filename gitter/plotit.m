figure(1);
clf;
axis equal;

hold on;

% Punkte plotten
plot(Point(:,1),Point(:,2),'r+')
plot(NewPoint(:,1),NewPoint(:,2),'b+')

% Kanten plotten
for ii = 1:size(Edge,1)
    if sum(Edge(ii,:)==0) == 0
        plot(Point(Edge(ii,:),1),Point(Edge(ii,:),2),'g-')
        text(sum(Point(Edge(ii,:),1))/2,sum(Point(Edge(ii,:),2))/2,num2str(ii));
    end
end
