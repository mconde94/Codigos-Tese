function [OutGrid, Out] = CircleNetwork(NumberOfAgents,Neighbours)
OutGrid=diag(ones(NumberOfAgents,1));
k=Neighbours;
for k=1:Neighbours
    for i=1:NumberOfAgents
        for j=1:NumberOfAgents
            if i==j
                if  i-k>=1 && i+k<=NumberOfAgents
                    OutGrid(j-k,i)=1;
                    OutGrid(j,i-k)=1;
                    OutGrid(j+k,i)=1;
                    OutGrid(j,i+k)=1;
                end
            end
        end
    end
end
Table=zeros(NumberOfAgents,2);
for i=1:NumberOfAgents
    count=0;
    for j=1:NumberOfAgents
        if OutGrid(i,j)~=0
            count=count+1;
        end
    end
    Table(i,1)=count;
end
Table(:,2)=1+2*Neighbours;
Table=Table(:,2)-Table(:,1);
for i=1:NumberOfAgents
    if Table(i)~=0
        Place=Table(i);
        if OutGrid(i,1)~=0
            for k=1:Place
                OutGrid(i,NumberOfAgents-k+1)=1;
            end
        elseif OutGrid(i,NumberOfAgents)~=0
            for k=1:Place
                OutGrid(i,k)=1;
            end
        end
    end
end
OutGrid=OutGrid-diag(ones(NumberOfAgents,1));
Out=zeros(NumberOfAgents,2*Neighbours);
for i=1:NumberOfAgents
    k=1;
    for j=1:NumberOfAgents
        if OutGrid(i,j)==1
            Out(i,k)=j;
            k=k+1;
        end
    end
end
end