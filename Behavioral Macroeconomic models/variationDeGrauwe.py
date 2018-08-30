from SIMULATIONS import *

N = 100
ListaStdR= np.zeros((N,1))
ListaMeanR = np.zeros((N,1))
ListaKurtR = np.zeros((N,1))
'''
ListaStdY = np.zeros((N,1))
ListaStdP = np.zeros((N,1))
ListaStdAS = np.zeros((N,1))
ListaACorrY= np.zeros((N,1))
ListaACorrP= np.zeros((N,1))
ListaCorrYS = np.zeros((N,1))
ListaMeanAS = np.zeros((N,1))
ListaMeanY = np.zeros((N,1))
ListaMeanP = np.zeros((N,1))
ListaKurtY = np.zeros((N,1))
ListaKurtP = np.zeros((N,1))
'''

numAgentes = int(np.sum(np.genfromtxt('America.csv', delimiter=',')) + 1)
topologia = 'AmericaS'

c1 = 2
c2 = 2
interaction = 'DeGrauwe'
#numAgentes = 650
#topologia = 'Circular'
Temp = 100

for i in range(0,N):
    sim = Simulation(interaction, numAgentes, topologia, c1, c2)
    sim.Gamma = Temp
    sim.MakeSimulation()
    ListaStdR[i]=np.std(sim.InterestRateTR)
    ListaMeanR[i]=np.mean(sim.InterestRateTR)
    ListaKurtR[i]=float(stats.kurtosis(sim.InterestRateTR))
    '''
    sim.AllStatisticalTests()
    ListaStdP[i]=sim.StdP
    ListaStdY[i]=sim.StdY
    ListaStdAS[i]=sim.StdAS
    ListaACorrY[i]=sim.AutoCorrY[1][0]
    ListaACorrP[i]=sim.AutoCorrP[1][0]
    ListaCorrYS[i]=sim.CorrYS
    ListaMeanAS[i]=sim.MeanAS
    ListaMeanY[i]=sim.MeanY
    ListaMeanP[i]=sim.MeanP
    ListaKurtY[i]=sim.KurtY
    ListaKurtP[i]=sim.KurtP

fig1 = plt.figure(1)
MakeAnHistogram(ListaStdY,'Standard deviation of the ouput gap',15)
fig2 = plt.figure(2)
MakeAnHistogram(ListaStdP,'Standard deviation of the inflation',15)

sim = Simulation(interaction, numAgentes, topologia, c1, c2)
sim.Gamma = Temp
sim.MakeSimulation()
sim.AllStatisticalTests()
sim.TimeSeriesGraph(3)
sim.FrequencyGraphOfTimeSeries(7, 20)
'''


print('desvio padrao')
print(np.mean(ListaStdR))
print('media')
print(np.mean(ListaMeanR))
print('kurtosis')
print(np.mean(ListaKurtR))