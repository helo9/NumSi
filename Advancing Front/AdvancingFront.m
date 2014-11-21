clear all

global Point Edge Triangle NewPoint

% Gebiet definieren
Point(1,:) = [1,1];
Point(2,:) = [0,2];
Point(3,:) = [1,5];
Point(4,:) = [3,5];
Point(5,:) = [6,3];
Point(6,:) = [8,3];
Point(7,:) = [8,1];
Point(8,:) = [5,0];

temp = round(1:0.5:8);
temp(end+1) = 1;
Edge = reshape(temp,2,8)'; % hatte kb 1,2;2,3;3,4;... usw zu schreiben
Triangle = [];
NewPoint = [3,3;5,2];

% Front definieren
Front = [1:length(Edge)];


plotit;
waitforbuttonpress();

% Fortfahren bis alle Neuen Punkte verwurstet sind
while size(Front,2) > 3  
    
    curEdgeid = Front(end);
    Front(end) = [];
    
    %% Punkt auswÃ¤hlen
    
    % besten Punkt in Front finden
    pids = unique(Edge(Front(:),:)); 
    pids = pids(pids ~= Edge(curEdgeid,1) & pids ~= Edge(curEdgeid,2) ); % Punkte der aktuellen Kante rausnehmen
      
    
    P1 = Point(Edge(curEdgeid,1),:);
    P2 = Point(Edge(curEdgeid,2),:);
    
    % Punkte werden überprüft ob sie ein legales Dreieck bilden
    
    pidscopy = pids;
    pids = [];
    for i = 1:size(pidscopy,1)
        if check(P1,P2,Point(pidscopy(i),:))
            pids = [pids; pidscopy(i)]; 
        end
    end
    
    % Optimum fÃ¼r Front
    [foptvalue,foptid] = min(evaluate(P1,P2,Point(pids,:)));
    foptid = pids(foptid);
    
    % besten Punkt in NewPoint finden
    if length(NewPoint) > 0
        [npoptvalue,npoptid] = min(evaluate(P1,P2,NewPoint));
    else
        npoptvalue = foptvalue+1;
    end %if
    
    if(foptvalue <= npoptvalue  )
        % Verbindung mit Knoten in Front
        if isPointinEdge(foptid,Front(1))
            opid = setdiff(Edge(curEdgeid,:),Edge(Front(1),:));
            eid = addEdge(opid,foptid);
            Triangle(end+1,:) = [Front(1),curEdgeid,eid];
            Front(1) = [];
            Front(end+1) = eid;
        elseif isPointinEdge(foptid,Front(end))
            opid = setdiff(Edge(curEdgeid,:),Edge(Front(end),:));
            eid = addEdge(foptid,opid);
            Triangle(end+1,:) = [Front(end),curEdgeid,eid];
            Front(end) = [];
            Front(end+1) = eid;
        elseif isPointinEdge(foptid,Front(2))
            opid = setdiff(Edge(curEdgeid,:),Edge(Front(1),:));
            eid = addEdge(opid,foptid);
            eid2 = addEdge(setdiff(Edge(curEdgeid,:),opid),foptid);
            Triangle(end+1,:) = [Front(1),curEdgeid,eid];
            Triangle(end+1,:) = [Front(1),Front(2),eid2];
            Front([1,2]) = [];
            Front(end+1) = eid;
        elseif isPointinEdge(foptid,Front(end-1))
            opid = setdiff(Edge(curEdgeid,:),Edge(Front(end),:));
            eid = addEdge(foptid,opid);
            eid2 = addEdge(setdiff(Edge(curEdgeid,:),opid),foptid);
            Triangle(end+1,:) = [Front(end),curEdgeid,eid];
            Triangle(end+1,:) = [Front(end),Front(end-1),eid2];
            Front([end-1,end]) = [];
            Front(end+1) = eid;
        else
            error('Gebiet trennt sich in 2 Teilgebiete auf evtl. rekursiver aufruf Implementieren!!!')
        end %if
    else
        % Verbindung mit neuem Knoten
        Point(end+1,:) = NewPoint(npoptid,:);
        NewPoint(npoptid,:) = [];
        eid1 = addEdge(Edge(curEdgeid,1),length(Point));
        eid2 = addEdge(length(Point),Edge(curEdgeid,2));
        Triangle(end+1,:) = [curEdgeid,eid1,eid2];
        Front(end+1) = eid1;
        Front(end+1) = eid2;
    end %if

    plotit;
    waitforbuttonpress();
    
end %while

% letztes Dreieck hinzufÃ¼gen wenn man lustig is
