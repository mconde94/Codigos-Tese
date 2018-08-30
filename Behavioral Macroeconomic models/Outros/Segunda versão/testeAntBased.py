from SIMULATIONS import *

c1 = 1.5
c2 = 0.5
interaction = 'Ising'
numAgentes = 100
topologia = 'Circular'
sim = Simulation(interaction, numAgentes, topologia, c1, c2)
sim.IsingAntBasedSimulation()
sim.SetSTDOutputGap()
sim.TimeSeriesGraph(0)