from files import *

#parametros do modelo
CycleTime=300
CycleAgent='Boltzmann'
CycleGamma = 100   #parametro de mudanca gama no modelo de Brock Hommes
CycleInflationTarget= 2.0 #inflacao desejada do banco central
CycleEpRational=0.0 #previsao racional da inflacao (=1)
CycleEpExtrapol=0.0 #previsao extrapolativa da inflacao (=1)
CycleA1 = 0.5 #coeficiente do output esperado na eq do output gap
CycleA2 = -0.2 #elasticidade da taxa de juro na eq do output gap
CycleB1 = 0.5 #coeficiente da inflacao esperada na eq da inflacao
CycleB2 = 0.05 #coeficiente de output na eq da inflacao
CycleC1 = 1.5 #coeficiente da inflacao na eq de Taylor
CycleC2 = 0.5 #coeficiente do outputgap na eq de Taylor
CycleC3 = 0.5 #parametro de suavidade da taxa de juro eq de Taylor
CycleSigma1 = 0.5   #desvio padrao choque da eq do output gap
CycleSigma2 = 0.5   #desvio padrao choque da eq da inflacao
CycleSigma3 = 0.5   #desvio padrao choque da eq de Taylor
CycleRho=0.5   #ro na media dos erros quadrados
CycleRhoOut=0   #ro nos choques na eq do output gap
CycleRhoInf=0 #ro nos choques na eq da inflacao
CycleRhoTayl=0 #ro nos choques na equacao de Taylor
CycleRhoBH=0.5 #ro do modelo de Brock Homes
Cycle=Simulation(CycleTime,CycleAgent,CycleGamma,CycleInflationTarget,CycleEpRational,CycleEpExtrapol,CycleA1,CycleA2,CycleB1,CycleB2,CycleC1,CycleC2,CycleC3,CycleSigma1,CycleSigma2,CycleSigma3,CycleRho,CycleRhoOut,CycleRhoInf,CycleRhoTayl,CycleRhoBH)
Cycle.SingleSimulationOriginal()
Cycle.StatisticalTest()
Cycle.TimeSeriesGraph(0)
Cycle.FrequencyGraphOfTimeSeries(4)