polar1=[-5,1];
polar2=[5,1];
delta_r=0.3;
num_of_circle=50;
min_r=(polar2(1)-polar1(1))/2;

plot(polar1(1),polar1(2),'ro');
hold on;
plot(polar2(1),polar2(2),'ro');
for n = [0:num_of_circle]
    r=min_r+n*delta_r;
    rectangle('position',[polar1(1)-r,polar1(2)-r,2*r,2*r],'curvature',[1,1]);
    rectangle('position',[polar2(1)-r,polar2(2)-r,2*r,2*r],'curvature',[1,1]);
end
rectangle('position',[polar1(1),polar1(2)-r+delta_r,polar2(1)-polar1(1),r-min_r],'edgecolor','r')
hold off;