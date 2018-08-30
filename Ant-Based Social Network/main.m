clc;
clear all;

numSpins =250; %dimension of array
numNeigh=2;%number of Neighbours
[~,Neighbours]=CircleNetwork(numSpins,numNeigh);
numIters=10000;

selfExp=0.25;
J = 1;%magnetic atomic momenta
h=1; %externalmagneticfield
mumomenta=1; %self magnetization

% Temperatures to sample
numTemps = 2^16;
kT = linspace(0, 1000, numTemps);
probSpinUp = 0.5;

ChainSpins=zeros(numTemps,numSpins);

% Preallocate to store results
Mstd=zeros(size(kT));
Mmean = zeros(size(kT));
MgSuspVar=zeros(size(kT));
ErrorEntropy=zeros(size(kT));


parfor tempIndex = 1 : numTemps
    spin = GridBuilding(numSpins, probSpinUp);
    spin= metropolisEquilibrium(numIters,spin,Neighbours, kT(tempIndex), J,h,mumomenta,selfExp);
    [spin,Magnetizations] = metropolisSampling(numIters,spin,Neighbours, kT(tempIndex),J,h,mumomenta,selfExp);
    Mstd(tempIndex) =std(Magnetizations);
    Mmean(tempIndex) = mean(Magnetizations);
    MgSuspVar(tempIndex) = suspIsing(Magnetizations,kT(tempIndex));
    ErrorEntropy(tempIndex)=wentropy(Magnetizations,'shannon')/numel(spin);
    ChainSpins(tempIndex,:)=spin;
end

figure(1);
subplot(2,1,1);
plot(kT, Mmean, '.');
title('Mean Magnetization Per Spin vs Interaction');
xlabel('\lambda⁻¹');
ylabel('<M>');


subplot(2,2,3);
plot(kT, MgSuspVar, '.');
title('Magnetic Susceptibility Per Spin vs Interaction');
xlabel('\lambda⁻¹');
ylabel('\chi');

subplot(2,2,4);
plot(kT, ErrorEntropy, '.');
title('Entropy vs Interaction');
xlabel('λ⁻¹');
ylabel('Entropy');
