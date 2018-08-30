function spin= metropolisEquilibrium(numIters,spin,Neighbours, kT, J,h,mumomenta)


for iter = 1 : numIters
    % Pick a random spin
    Index = randi(numel(spin));
    nn=Neighbours(Index,:);    
    % Calculate energy change if this spin is flipped
    dE = 2 * J * spin(Index) * sum(spin(nn));
    
    dE=dE+(mumomenta+h)*spin(Index);
    % Boltzmann probability of flipping
    prob = exp(-dE / kT);
    
    % Spin flip condition
    if dE <= 0 || rand() <= prob
        spin(Index) = - spin(Index);
    end
    
end

end
