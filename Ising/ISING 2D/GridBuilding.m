function spin = GridBuilding(numSpinsPerDim, p)
spin = sign(p - rand(numSpinsPerDim, numSpinsPerDim));
end