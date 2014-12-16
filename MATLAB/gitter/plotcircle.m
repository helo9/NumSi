function plotcircle(center,radius,color)

figure(1)
hold on
xmitte=center(1);
ymitte=center(2);
 
phi=1:1:360;
phi=phi./180.*pi;
[xtmp,ytmp] = pol2cart(phi,radius); 
x=xtmp+xmitte;
y=ytmp+ymitte;
 
plot(x,y,color)

end %function