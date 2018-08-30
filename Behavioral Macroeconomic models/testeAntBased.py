from SIMULATIONS import *

c1 = 1.5
c2 = 1.5
interaction = 'Ising'
numAgentes = int(np.sum(np.genfromtxt('America.csv', delimiter=',')) + 1)
topologia = 'AmericaC'
sim = Simulation(interaction, numAgentes, topologia, c1, c2)
sim.Grid.ImitationRate = 0.6
sim.Grid.SelfConversion = 0.15
sim.Grid.OutConversion = 1
sim.Gamma = 75
sim.ConstantSigma1 = 0.5
sim.ConstantSigma2 = 0.5
sim.ConstantSigma3 = 0.5
sim.MakeSimulation()
sim.AllStatisticalTests()
sim.TimeSeriesGraph(0)
sim.FrequencyGraphOfTimeSeries(4, 20)
