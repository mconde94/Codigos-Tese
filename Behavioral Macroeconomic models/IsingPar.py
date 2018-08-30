from SIMULATIONS import *

#achar a politica monetaria otima para a interacao ising/ant-based

start_time = time.time()

interaction = 'Ising'
numeroAgentes = int(np.sum(np.genfromtxt('America.csv', delimiter=',')) + 1)
topologia = 'AmericaS'


def OptimalPolicy(cc1, cc2):
    sim = Simulation(interaction, numeroAgentes, topologia, cc1, cc2)
    sim.Grid.ImitationRate = 0.6
    sim.Grid.SelfConversion = 0.15
    sim.Grid.OutConversion = 0.1
    sim.Gamma = 10
    sim.MakeSimulation()
    sim.SomeStatisticalTests()
    resultado = Result(sim)
    return resultado


def OptimalPolicyHelper(args):
    return OptimalPolicy(*args)


def ParalellOptimalPolicy(list_c1, list_c2):
    # nao especificar o numero de processos usa o maximo numero de cores
    p1 = mp.Pool()
    # preparar os inputs como tuplas
    job_args = [(item_c1, list_c2[i]) for i, item_c1 in enumerate(list_c1)]
    # fazer o ciclo
    o1 = p1.map(OptimalPolicyHelper, job_args)
    return o1


bc = 0.1  # inicio dos c
step = 0.1  # step dos c
ec = 3  # final do c
N = 50  # numero de c para fazer a media
nf = int(round(1 + (ec - bc) / step))
list_c1, list_c2 = VectorParallel(bc, ec + step, step, N)
c1 = np.linspace(bc, ec, nf)
c2 = np.linspace(bc, ec, nf)
tamanho = np.size(list_c1)
mediasY = np.zeros((nf + 1, nf + 1))
mediasP = np.zeros((nf+1,nf+1))
# ciclo for paralelizado
data = ParalellOptimalPolicy(list_c1, list_c2)

# organizar os dados
for i in range(0, tamanho):
    indexcc1 = int(round((data[i].C1 - bc) / step))
    indexcc2 = int(round((data[i].C2 - bc) / step))
    mediasY[indexcc1, indexcc2] = mediasY[indexcc1, indexcc2] + data[i].OutputGapSD
    mediasP[indexcc1, indexcc2] = mediasP[indexcc1, indexcc2] + data[i].InflationSD
mediasY = mediasY / N
mediasP = mediasP / N
mediasY = mediasY[0:(np.size(c1)), 0:(np.size(c1))]
mediasP = mediasP[0:(np.size(c1)), 0:(np.size(c1))]


algumextra='ISING3'

# guardar como ficheiro .mat que os graficos ficam mais bonitos no matlab
# mover para o diretorio do matlab
now = datetime.datetime.now()
nome = algumextra + 'Hora' + str(now.hour) + 'Dia' + str(now.day) + 'Mes' + str(now.month) + 'Ano' + str(
    now.year) + interaction + topologia + str(numeroAgentes) + 'Agents' + '.mat'
nomefig = 'Hora' + str(now.hour) + 'Dia' + str(now.day) + 'Mes' + str(now.month) + 'Ano' + str(
    now.year) + interaction + topologia + str(numeroAgentes) + 'Agents'+'.png'
sio.savemat(nome, mdict={'mediasY': mediasY,'mediasP': mediasP, 'c1': c1, 'c2': c2,'nomefig':nomefig})
print('Finish')
print("--- %s seconds ---" % (time.time() - start_time))
