from files import *
#parametros do modelo
n=5000 #n repeticoes
step=0.05
Start=0.1
End=5
CycleTime=10
CycleAgent='Boltzmann'
CycleGamma = 1 #parametro de mudanca gama no modelo de Brock Hommes
CycleInflationTarget= 2 #inflacao desejada do banco central
CycleEpRational=0 #previsao racional da inflacao (=1)
CycleEpExtrapol=0 #previsao extrapolativa da inflacao (=1)
CycleA1 = 0.5 #coeficiente do output esperado na eq do output gap
CycleA2 = -0.0 #elasticidade da taxa de juro na eq do output gap
CycleB1 = 0.5#coeficiente da inflacao esperada na eq da inflacao
CycleB2 = 0.05 #coeficiente de output na eq da inflacao
CycleC2 = 0.5 #coeficiente do outputgap na eq de Taylor
CycleC3 = 0.5 #parametro de suavidade da taxa de juro eq de Taylor
CycleSigma1 = 0.1   #desvio padrao choque da eq do output gap
CycleSigma2 = 0.1   #desvio padrao choque da eq da inflacao
CycleSigma3 = 0.1   #desvio padrao choque da eq de Taylor
CycleRho=0.5   #ro na media dos erros quadrados
CycleRhoOut=0.0   #ro nos choques na eq do output gap
CycleRhoInf=0.0   #ro nos choques na eq da inflacao
CycleRhoTayl=0.0   #ro nos choques na equacao de Taylor
CycleRhoBH=0.0   #ro do modelo de Brock Homes
N=int((End-Start+step)/step)
valueY=np.zeros(N)
valueP=np.zeros(N)
SIMULATIONS = []
j=0
for CycleC1 in frange (Start, End, step):
    StdVectorY=np.zeros(n)
    StdVectorP=np.zeros(n)
    test=0
    for i in range (n):
        Cycle=Simulation(CycleTime,CycleAgent,CycleGamma,CycleInflationTarget,CycleEpRational,CycleEpExtrapol,CycleA1,CycleA2,CycleB1,CycleB2,CycleC1,CycleC2,CycleC3,CycleSigma1,CycleSigma2,CycleSigma3,CycleRho,CycleRhoOut,CycleRhoInf,CycleRhoTayl,CycleRhoBH)
        Cycle.SingleSimulationOriginal()
        Cycle.StatisticalTest()
        StdVectorY[i]=Cycle.StandardDeviationY
        StdVectorP[i]=Cycle.StandardDeviationP
        test=Cycle
    MeanY=np.mean(StdVectorY)
    MeanP=np.mean(StdVectorP)
    valueY[j]=MeanY
    valueP[j]=MeanP
    SIMULATIONS.append(test)
    j=j+1
IndexOptimalOutputGapY=np.argmin(valueY)
IndexOptimalInflationP=np.argmin(valueP)
OptimalOutputGapY=SIMULATIONS[IndexOptimalOutputGapY]
OptimalInflationP=SIMULATIONS[IndexOptimalInflationP]
print('=========== Optimal values for Output Gap ===========')
OptimalOutputGapY.PolicyPrint()
print('=========== Optimal values for Inflation ============')
OptimalInflationP.PolicyPrint()
C1Var=np.arange(Start,End+step,step)
#plots
fig1 = plt.figure(1)
plt.plot(C1Var,valueY)
plt.ylabel('standard deviation of output gap')
plt.xlabel('C1')
fig1 = plt.figure(2)
plt.plot(C1Var,valueP)
plt.ylabel('standard deviation of inflation')
plt.xlabel('C1')