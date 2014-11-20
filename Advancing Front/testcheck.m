%Testcase 1
clear all

Point(1,1) = 0;
Point(1,2) = 0; 
Point(2,1) = 1; 
Point(2,2) = 0;
Edge(1,:) = [1 2];
NewPoint(1,1) = 0.5;
NewPoint(1,2) = 1;

NewPoint(2,1) = 0.25;
NewPoint(2,2) = 0.75;

plotit;
fprintf('case 1');
waitforbuttonpress;
 if check(Point(1,:),Point(2,:),NewPoint(1,:), Edge, Point, NewPoint) == 1 && check(Point(2,:), Point(1,:),NewPoint(1,:), Edge, Point, NewPoint) == 1
       Point
       Edge
       NewPoint
       fprintf('correct legal');
 else
     Point
       Edge
       NewPoint
       fprintf('incorrect illegal');
 end


%Testcase 2
clear all

Point(1,1) = 0;
Point(1,2) = 0; 
Point(2,1) = 1; 
Point(2,2) = 0;
Edge(1,:) = [1 2];
NewPoint(1,1) = 0.5;
NewPoint(1,2) = 1;

NewPoint(2,1) = 1.2;
NewPoint(2,2) = 2;
waitforbuttonpress;
plotit;
waitforbuttonpress;
fprintf('case 2');
 if check(Point(1,:),Point(2,:),NewPoint(1,:), Edge, Point, NewPoint) == 1 && check(Point(2,:), Point(1,:),NewPoint(1,:), Edge, Point, NewPoint) == 1
       Point
       Edge
       NewPoint
       fprintf('correct legal');
 else
     Point
       Edge
       NewPoint
       fprintf('incorrect illegal');
 end
 
 %Testcase 3
clear all

Point(1,1) = 0;
Point(1,2) = 0; 
Point(2,1) = 1; 
Point(2,2) = 0;
Edge(1,:) = [1 2];
NewPoint(1,1) = 0.5;
NewPoint(1,2) = 1;

NewPoint(2,1) = 0.5;
NewPoint(2,2) = 0.5;
waitforbuttonpress;
plotit;
waitforbuttonpress;
fprintf('case 3');
 if check(Point(1,:),Point(2,:),NewPoint(1,:), Edge, Point, NewPoint) == 0 && check(Point(2,:), Point(1,:),NewPoint(1,:), Edge, Point, NewPoint) == 0
       Point
       Edge
       NewPoint
       fprintf('correct illegal');
 else
     Point
       Edge
       NewPoint
       fprintf('incorrect legal');
 end


%Testcase 4
clear all

Point(1,1) = 0;
Point(1,2) = 0; 
Point(2,1) = 1; 
Point(2,2) = 0;
Edge(1,:) = [1 2];
NewPoint(1,1) = 0.5;
NewPoint(1,2) = 1;

Point(3,1) = 0;
Point(3,2) = 0.5; 
Point(4,1) = 1.1; 
Point(4,2) = 0.3;
Edge(2,:) = [3 4];

plotit;
fprintf('case4');
waitforbuttonpress;
 if check(Point(1,:),Point(2,:),NewPoint(1,:), Edge, Point, NewPoint) == 0 && check(Point(2,:), Point(1,:),NewPoint(1,:), Edge, Point, NewPoint) == 0
       Point
       Edge
       NewPoint
       fprintf('correct illegal');
 else
     Point
       Edge
       NewPoint
       fprintf('incorrect legal');
 end