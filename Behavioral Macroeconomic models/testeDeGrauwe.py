from SIMULATIONS import *

c2 = 0.1
c1 = 0.1
interaction = 'DeGrauwe'
#escolhe o maior AlfaY de todos os vizinhos
numAgentes = int(np.sum(np.genfromtxt('America.csv', delimiter=',')) + 1)
topologia = 'AmericaS'
sim = Simulation(interaction, numAgentes, topologia, c1, c2)
sim.Gamma = 100
sim.ConstantSigma1 = 0.5/1
sim.ConstantSigma2 = 0.5/1
sim.ConstantSigma3 = 0.5/1
sim.MakeSimulation()
sim.AllStatisticalTests()
print(sim.StdY)
sim.TimeSeriesGraph(0)
sim.FrequencyGraphOfTimeSeries(4, 30)
