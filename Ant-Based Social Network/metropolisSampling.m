function[ spin, ChainMagnetization]= metropolisSampling(numIters,spin,Neighbours, kT, J,h,mumomenta,selfExp)

old = spin;

lambda=1/kT;

ChainMagnetization = zeros(1,numIters);
    
for iter = 1 : numIters
    % Pick a random spin
    Index = randi(numel(spin));
    nn=Neighbours(Index,:);
    
    
    mi = selfExp*spin(Index)+2 * J  * sum(old(nn))/length(nn);
    
    mi=mi+mumomenta*h*spin(Index);
    %probability of flipping
    prob = 1/(1+exp(-2*mi * lambda));    
    if old(Index)==-1  
        alfa=min(1,prob);
    else
        alfa=min(1,1-prob);
    end

    % Expectative flip condition
    if mi <= 0 || rand() <= alfa
        spin(Index) = - spin(Index);
    end
    
    %chain values
    ChainMagnetization(iter)= mean(spin(:));
    
end

end