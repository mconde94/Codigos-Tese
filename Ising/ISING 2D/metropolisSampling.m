function[ spin, ChainEnergy, ChainMagnetization]= metropolisSampling(numIters,spin, kT, J,h,mumomenta)

ChainEnergy = zeros(1,numIters);
ChainMagnetization = zeros(1,numIters);

    
for iter = 1 : numIters
    % Pick a random spin
    linearIndex = randi(numel(spin));
    [row, col]  = ind2sub(size(spin), linearIndex);
    
    % Find its nearest neighbors
    above = mod(row - 1 - 1, size(spin,1)) + 1;
    below = mod(row + 1 - 1, size(spin,1)) + 1;
    left  = mod(col - 1 - 1, size(spin,2)) + 1;
    right = mod(col + 1 - 1, size(spin,2)) + 1;
    
    neighbors = [      spin(above,col);
        spin(row,left);                spin(row,right);
                       spin(below,col)];
    
    % Calculate energy change if this spin is flipped
    dE = 2 * J * spin(row, col) * sum(neighbors);
    
    dE=dE+mumomenta*h*spin(row, col);
    % Boltzmann probability of flipping
    prob = exp(-dE / kT);
    
    % Spin flip condition
    if dE <= 0 || rand() <= prob
        spin(row, col) = - spin(row, col);
    end
    
    %chain values
    ChainEnergy(iter)= Hamiltonian(spin, J,h,mumomenta);
    ChainMagnetization(iter)= mean(spin(:));
    
end

end
