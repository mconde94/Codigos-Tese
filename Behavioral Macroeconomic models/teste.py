from SIMULATIONS import *

c1 = 1.5
c2 = 0.5
interaction = 'Ising'
numAgentes = int(np.sum(np.genfromtxt('America.csv', delimiter=',')) + 1)
topologia = 'Random'
sim = Simulation(interaction, numAgentes, topologia, c1, c2)
sim.MakeSimulation()
sim.SetSTDOutputGap()
sim.TimeSeriesGraph(0)
sim.FrequencyGraphOfTimeSeries(4,30)