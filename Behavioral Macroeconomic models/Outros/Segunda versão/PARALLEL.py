from SIMULATIONS import *

def OptimalPolicy(cc1, cc2,interaction,numeroAgentes,topologia):
    sim = Simulation(interaction, numeroAgentes, topologia, cc1, cc2)
    if interaction is 'DeGrauwe':
        sim.DeGrauweSimulation()
    else:
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