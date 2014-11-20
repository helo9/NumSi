clear all

global Point Edge Triangle

Point(1,1) = 0; 
Point(1,2) = 0; 

Point(2,1) = 0; 
Point(2,2) = 1;

Point(3,1) = 0.5;
Point(3,2) = 2;

Point(4,1) = 1.5;
Point(4,2) = 2;

Point(5,1) = 1;
Point(5,2) = 1;

Point(6,1) = 2;
Point(6,2) = 0;

Edge(1,:) = [1 2];
Edge(2,:) = [2 3];
Edge(3,:) = [3 4];
Edge(4,:) = [4 6];
Edge(5,:) = [1 6];
Edge(6,:) = [1 5];
Edge(7,:) = [5 6];
Edge(8,:) = [2 5];
Edge(9,:) = [4 5];
Edge(10,:) = [3 5];

Triangle(1,:) = [1 6 8];
Triangle(2,:) = [2 8 10];
Triangle(3,:) = [3 9 10];
Triangle(4,:) = [4 7 9];
Triangle(5,:) = [5 6 7];

NewPoint(1,1) = 0.5;
NewPoint(1,2) = 0.5;

NewPoint(2,1) = 1.5;
NewPoint(2,2) = 1;

NewPoint(3,1) = 1.25;
NewPoint(3,2) = 0.5;

NewPoint(4,:) = [0.5,1.5];

NewPoint(5,:) = [0.8,0.5];

% Daten sortieren
Edge = sort(Edge,2);
Triangle = sort(Triangle,2);

for main_ii = 1:size(NewPoint,1)
    
    % aktPoint => hinzu zu fügender Punkt
    Point(end+1,:) = NewPoint(main_ii,:);
    
    % Plotten
    plotit;
    
    % Dreiecke finden, deren Umkreis neuen aktPoint beinhaltet
    badTriangle = [];
    
    for main_jj = [1:size(Triangle,1)]
    
        aktTrianglePts = getTrianglePointIdx(Triangle(main_jj,:));
        
        
        [center, radius] = getcircumcircle(Point(aktTrianglePts(1),:)...
            ,Point(aktTrianglePts(2),:),Point(aktTrianglePts(3),:));
        
        if norm(Point(end,:) - center) <= radius
            badTriangle(end+1,:) = main_jj;
            plotcircle(center,radius,'c');
        else
            plotcircle(center,radius,'k:');            
        end
    end
    
    waitforbuttonpress;
    
    % Polygon aus Dreiecken erstellen
    poly = [];
    delEdges = [];
    
    % Dreiecke durch iterieren
    for main_kk = 1:size(badTriangle,1)
        % über Kanten der Dreiecke interieren
        for main_jj = 1:3
            
            % Kante schon im Polygon vorhanden -> doppelte Kante, Löschen
            aktEdgeIndex = Triangle(badTriangle(main_kk),main_jj);
            
            index = find(poly== aktEdgeIndex);
            
            if ~isempty(index)
                % doppelte Kante Löschen
                deleteEdge(aktEdgeIndex);
                poly(index) = [];
                poly = poly - (poly > aktEdgeIndex);
            else
                % ansonsten zum neuen Polygon hinzufügen
                poly(end+1) = aktEdgeIndex;
            end %if
        end %for
    end % for
    
    plotit;
    
    for main_kk = 1:length(poly)
        plot(Point(Edge(poly(main_kk),:),1),Point(Edge(poly(main_kk),:),2),'r');
    end %for
    
    waitforbuttonpress;
    
    % badTriangles löschen
    Triangle(badTriangle,:) = [];
    
    %erstes Dreieck hinzufügen
    Edge(end+1,:) = sort([Edge(poly(1),1),length(Point)]);
    Edge(end+1,:) = sort([Edge(poly(1),2),length(Point)]);
    Triangle(end+1,:) = sort([poly(1),length(Edge)-1,length(Edge)]);
    
    % Verbindungspunkt zwischen letzter und neuer Kante
    ConPointIndex = Edge(poly(1),2);
    StartEdgeIndex = length(Edge)-1;
    
    % Kante aus ungeordnetem Polygon löschen
    poly(1) = [];
    
    % Geordnetes Polygon schrittweise füllen
    for main_jj = 1:length(poly)
        
        if length(poly) == 1
            Triangle(end+1,:) = sort([StartEdgeIndex,poly(1),length(Edge)]);
        else
        
            % nächste Kante finden, die ConPoint enthält      
            [EdgeinPolyId,PtinEdgeId] = find(Edge(poly,:)==ConPointIndex);
      
            OtherPtinEdgeId = ~(PtinEdgeId-1)+1;
            OtherPtId = Edge(poly(EdgeinPolyId),OtherPtinEdgeId);
                    
            Edge(end+1,:) = sort([OtherPtId,length(Point)]);
            Triangle(end+1,:) = sort([poly(EdgeinPolyId),length(Edge)-1,length(Edge)]);
            ConPointIndex = Edge(poly(EdgeinPolyId),OtherPtinEdgeId);
            poly(EdgeinPolyId) = [];
        end %if
    end  %for
    plotit;
    waitforbuttonpress;
end
