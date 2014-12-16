figure(1);
clf;
axis equal;

hold on;

% Punkte plotten
plot(Point(:,1),Point(:,2),'r+')
for ii = 1:size(Point,1)
    text(Point(ii,1),Point(ii,2),num2str(ii),'color','r')
end %for

if length(NewPoint) > 0
    plot(NewPoint(:,1),NewPoint(:,2),'b+')
end %if

% Kanten plotten
for ii = 1:size(Edge,1)
    if sum(Edge(ii,:)==0) == 0
        plot(Point(Edge(ii,:),1),Point(Edge(ii,:),2),'g-')
        %text(sum(Point(Edge(ii,:),1))/2,sum(Point(Edge(ii,:),2))/2,num2str(ii));
    end
end

% Front plotten
for ii = 1:size(Front,2)
    plot(Point(Edge(Front(ii),:),1),Point(Edge(Front(ii),:),2),'r-')
    text(sum(Point(Edge(Front(ii),:),1))/2,sum(Point(Edge(Front(ii),:),2))/2,[num2str(ii) '-' num2str(Front(ii))]);
end
