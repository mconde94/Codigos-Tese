function spin = GridBuilding(numSpinsPerDim, p)
spin = sign(p - rand(1, numSpinsPerDim));
end