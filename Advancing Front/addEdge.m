function eid = addEdge(pid1,pid2)

global Edge

Edge(end+1,:) = [pid1,pid2];

eid = length(Edge);

end %function