clc;
clear all;

numSpins =1000; %dimension of array
numNeigh=1;%number of Neighbours
[~,Neighbours]=CircleNetwork(numSpins,numNeigh);
numIters=floor(numSpins*log(numSpins))*5;

J = 1;%magnetic atomic momenta
h=0; %externalmagneticfield
mumomenta=1; %self magnetization

% Temperatures to sample
numTemps = 2^11;
kTc = 2*J / log(1+sqrt(2)); % Curie temperature
kT = linspace(0, 3*kTc, numTemps);
probSpinUp = 1;

% Preallocate to store results
Emean = zeros(size(kT));
CvVar=zeros(size(kT));
Mmean = zeros(size(kT));
MgSuspVar=zeros(size(kT));
ErrorEntropy=zeros(size(kT));

parfor tempIndex = 1 : numTemps
    spin = GridBuilding(numSpins, probSpinUp);
    spin= metropolisEquilibrium(numIters,spin,Neighbours, kT(tempIndex), J,h,mumomenta);
    [spin,Energies,Magnetizations] = metropolisSampling(numIters,spin,Neighbours, kT(tempIndex), J,h,mumomenta);
    Emean(tempIndex) = mean(Energies/numSpins);
    CvVar(tempIndex) =cvIsing(Energies/numSpins,kT(tempIndex));
    Mmean(tempIndex) = mean(Magnetizations);
    MgSuspVar(tempIndex) = suspIsing(Magnetizations,kT(tempIndex));
    ErrorEntropy(tempIndex)=wentropy(Magnetizations,'shannon')/numSpins;
end


figure(1);
subplot(2,2,1);
plot(kT, Emean, '.');
title('Mean Energy Per Spin vs Temperature');
xlabel('kT'); 
ylabel('<E>');

subplot(2,2,2);
plot(kT, Mmean, '.');
title('Mean Magnetization Per Spin vs Temperature');
xlabel('kT');
ylabel('<M>');

subplot(2,3,4);
plot(kT, CvVar, '.');
title('Specific Heat Per Spin vs Temperature');
xlabel('kT');
ylabel('Cv');

subplot(2,3,6);
plot(kT, MgSuspVar, '.');
title('Magnetic Susceptibility Per Spin vs Temperature');
xlabel('kT');
ylabel('X');

subplot(2,3,5);
plot(kT, ErrorEntropy, '.');
title('Entropy vs Temperature');
xlabel('kT');
ylabel('Entropy');