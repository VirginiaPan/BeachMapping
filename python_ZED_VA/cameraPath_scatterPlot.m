%import data
M = csvread('translation.csv');
x = M(:,1);
y = M(:,2);
z = M(:,3);
time = M(:,4);
color = strings(length(x),1);
for i = 1:length(x)
    if(i<100)
        color(i) = 'r';
    elseif(100<=i<=length(x)-100)
        color(i) = 'y';
    else
        color(i) = 'b';
    end
end

%plot data
figure(1)
clf
scatter3(x,y,z)
%hold on
%plot3(x(end),y(end),z(end),'MarkerEdgeColor','red','MarkerFaceColor','red','MarkerSize', 15)
