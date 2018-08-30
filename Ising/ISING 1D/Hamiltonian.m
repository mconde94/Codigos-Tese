function Emean = Hamiltonian(spin,Neighbours, J,h,mumomenta)

sumOfNeighbors =  transpose(sum(Neighbours,2));
Em = - J *0.5 * spin .* sumOfNeighbors-h*mumomenta*spin;
Emean = sum(Em)/ numel(spin);
end