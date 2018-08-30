from NETWORKS import *

numAgentes = 100
interaction = 'Ising'
topologia = 'Circular'
iteracoes = numAgentes*10
gamma = np.linspace(0.0001,10,100)
valoresFinais = np.zeros((np.size(gamma),1))
for i in range(0,np.size(gamma)):
    current = np.zeros((iteracoes, 1))
    Grid = Network(numAgentes, interaction, topologia, iteracoes)
    for j in range (0,iteracoes):
        Grid.IsingInteraction(gamma[i],0,j)
        current[j] = Grid.Expectative
    valoresFinais[i] = np.mean(current[int(np.size(current)/2-1) :])
fig1 = plt.figure(1)
plt.plot(gamma, valoresFinais)
plt.ylabel('Magnetization')
plt.xlabel('Gamma')
plt.title('')
plt.show()