w=100;
delta=0.115;
ap=186.81;
bp=186.82;
aq=ap+delta;
bq=bp-delta;
x=(ap^2+w^2-bp^2)/(2*ap*w);
y=(aq^2+w^2-bq^2)/(2*aq*w);
d_sqr=ap^2+aq^2-2*ap*aq*(x*y+sqrt((1-x^2)*(1-y^2)));
d=sqrt(d_sqr)

