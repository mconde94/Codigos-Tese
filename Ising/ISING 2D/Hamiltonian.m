function Emean = Hamiltonian(spin, J,h,mumomenta)

sumOfNeighbors =  circshift(spin, [ 0  1]) +circshift(spin, [ 0 -1]) + circshift(spin, [ 1  0]) + circshift(spin, [-1  0]);
Em = - J *0.5* spin .* sumOfNeighbors-h*mumomenta*spin;
Emean = sum(Em(:)) / numel(spin);
end
