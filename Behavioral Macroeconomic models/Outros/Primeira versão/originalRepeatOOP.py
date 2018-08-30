from files import *
n=1000 #numero de repeticoes
#parametros do modelo
SIMULATIONS=[]
StdVectorY = np.zeros(n)
StdVectorP=np.zeros(n)
CycleTime=200
CycleAgent='Boltzmann'
CycleGamma = 1 #parametro de mudanca gama no modelo de Brock Hommes
CycleInflationTarget= 2 #inflacao desejada do banco central
CycleEpRational=0 #previsao racional da inflacao (=1)
CycleEpExtrapol=0 #previsao extrapolativa da inflacao (=1)
CycleA1 = 0.5 #coeficiente do output esperado na eq do output gap
CycleA2 = -0.0 #elasticidade da taxa de juro na eq do output gap
CycleB1 = 0.5#coeficiente da inflacao esperada na eq da inflacao
CycleB2 = 0.05 #coeficiente de output na eq da inflacao
CycleC1 = 1.5 #coeficiente da inflacao na eq de Taylor
CycleC2 = 0.5 #coeficiente do outputgap na eq de Taylor
CycleC3 = 0.5 #parametro de suavidade da taxa de juro eq de Taylor
CycleSigma1 = 0.5   #desvio padrao choque da eq do output gap
CycleSigma2 = 0.5   #desvio padrao choque da eq da inflacao
CycleSigma3 = 0.5   #desvio padrao choque da eq de Taylor
CycleRho=0.5   #ro na media dos erros quadrados
CycleRhoOut=0.0   #ro nos choques na eq do output gap
CycleRhoInf=0.0   #ro nos choques na eq da inflacao
CycleRhoTayl=0.0   #ro nos choques na equacao de Taylor
CycleRhoBH=0.0   #ro do modelo de Brock Homes
for i in range (n):
    Cycle=Simulation(CycleTime,CycleAgent,CycleGamma,CycleInflationTarget,CycleEpRational,CycleEpExtrapol,CycleA1,CycleA2,CycleB1,CycleB2,CycleC1,CycleC2,CycleC3,CycleSigma1,CycleSigma2,CycleSigma3,CycleRho,CycleRhoOut,CycleRhoInf,CycleRhoTayl,CycleRhoBH)
    Cycle.SingleSimulationOriginal()
    Cycle.StatisticalTest()
    SIMULATIONS.append(Cycle)
    StdVectorY[i]=Cycle.StandardDeviationY
    StdVectorP[i]=Cycle.StandardDeviationP
fig1 = plt.figure(1)
MakeAnHistogram(StdVectorY,'Frequency Distribution of the standard deviation of the Output Gap')
fig1 = plt.figure(2)
MakeAnHistogram(StdVectorP,'Frequency Distribution of the standard deviation of the Inflation')
