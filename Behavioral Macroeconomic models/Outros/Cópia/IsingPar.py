from SIMULATIONS import *

interaction = 'Ising'
topologia = 'Circular'
numeroAgentes = 10


def OptimalPolicy(cc1, cc2):
    sim = Simulation(interaction, numeroAgentes, topologia, cc1, cc2)
    sim.IsingAntBasedSimulation()
    sim.SetSTDOutputGap()
    return sim


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
N = 50 # numero de c para fazer a media
nf = int(round(1 + (ec - bc) / step))
list_c1, list_c2 = VectorParallel(bc, ec + step, step, N)
c1 = np.linspace(bc, ec, nf)
c2 = np.linspace(bc, ec, nf)
tamanho = np.size(list_c1)
medias = np.zeros((nf + 1, nf + 1))

# ciclo for paralelizado
data = ParalellOptimalPolicy(list_c1, list_c2)

# organizar os dados
for i in range(0, tamanho):
    indexcc1 = int(round((data[i].ConstantC1 - bc) / step))
    indexcc2 = int(round((data[i].ConstantC2 - bc) / step))
    medias[indexcc1, indexcc2] = medias[indexcc1, indexcc2] + data[i].StdY
medias = medias / N
medias = medias[0:(np.size(c1)), 0:(np.size(c1))]
nome = interaction + topologia + str(numeroAgentes) + 'Agents' + '.mat'


# guardar como ficheiro .mat que os graficos ficam mais bonitos no matlab
# mover para o diretorio do matlab
sio.savemat(nome, mdict={'medias': medias, 'c1': c1, 'c2': c2})
source_files = '/home/manuel/Dropbox/Python/Tese/'+ nome
destination_folder = '/home/manuel/Dropbox/MATLAB/Tese/'+nome
os.rename(source_files, destination_folder)
print('Finish')
