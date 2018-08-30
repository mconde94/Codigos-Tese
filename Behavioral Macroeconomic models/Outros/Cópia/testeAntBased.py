from SIMULATIONS import *

c1=1.5
c2=0.5
sim = Simulation('DeGrauwe', 100, 'Circular', c1, c2)
sim.IsingAntBasedSimulation()
sim.SetSTDOutputGap()
sim.TimeSeriesGraph(0)