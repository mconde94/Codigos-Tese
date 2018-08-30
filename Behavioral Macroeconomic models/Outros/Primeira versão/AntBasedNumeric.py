from SIMULATIONS import *
#este codigo usava metodos numericos ideia que entretanto abandonei
def OPTIMUM(C):
    c1=C[0]
    c2=C[1]
    N = 100
    valor=np.zeros((N,1))
    for n in range(0, N):
        sim = Simulation('Ising', 100, 'Circular', c1, c2)
        sim.IsingAntBasedSimulation()
        sim.SetSTDOutputGap()
        valor[n] = sim.StdY
    return np.mean(valor)
algo='SLSQP'
tolerance=0.1
print('Running '+algo+' algorithm:')
start_time = time.time()
guess=( 1.5,0.5 )
bnds = ((0, 3), (0, 3))
res = minimize(OPTIMUM , guess, method=algo, bounds=bnds, tol=tolerance)
print('This algorithm takes:')
print("--- %s seconds ---" % (time.time() - start_time))
print('Result:')
print(res)