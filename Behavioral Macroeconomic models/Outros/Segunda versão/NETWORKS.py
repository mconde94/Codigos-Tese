from AGENTS import *


class Network:
    NumberOfAgents = None
    Topology = None
    CircularOrder = 2
    RandomNeighbours = 4
    Structure = None
    TypeOfInteraction = None
    List = []
    SelfConversion = 0.15  # self-conversion rate on the Ising Model
    ImitationRate = 0.7  # imititation rate on the Ising Model
    OutConversion=0.7
    Expectative = None

    def __init__(self, n, i, t, tempo):
        self.NumberOfAgents = n
        self.TypeOfInteraction = i
        self.Topology = t
        self.List = 2 * np.zeros(self.NumberOfAgents, dtype=Agent)
        for i in range(0, self.NumberOfAgents):
            self.List[i] = Agent(i, tempo)
        if self.Topology is 'Star':
            self.SetStarNetwork()
        elif self.Topology is 'Perfect':
            self.SetPerfectNetwork()
        elif self.Topology is 'Self':
            self.SetSelfNetwork()
        elif self.Topology is 'Circular':
            self.SetCircularNetwork()
        elif self.Topology is 'Random':
            self.SetRandomNetwork()
        elif self.Topology is 'Line':
            self.SetLineNetwork()

    def ActualizeNeighbours(self):
        for i in range(0, self.NumberOfAgents):
            self.SetNeighbours(i)

    def SetNeighbours(self, z):
        self.List[z].Neighbours = GetNeighbours(self.Structure, z)

    def Connect2Indexes(self, index1, index2):
        self.Structure[index1, index2] = 1
        self.Structure[index2, index1] = 1

    def SetStarNetwork(self):
        self.Structure = StarNetwork(self.NumberOfAgents)
        self.ActualizeNeighbours()

    def SetPerfectNetwork(self):
        self.Structure = PerfectNetwork(self.NumberOfAgents)
        self.ActualizeNeighbours()

    def SetSelfNetwork(self):
        self.Structure = SelfNetwork(self.NumberOfAgents)
        self.ActualizeNeighbours()

    def SetCircularNetwork(self):
        self.Structure = CircularNetwork(self.NumberOfAgents, self.CircularOrder)
        self.ActualizeNeighbours()

    def SetRandomNetwork(self):
        N = self.NumberOfAgents
        k = self.RandomNeighbours
        self.Structure = RandomNetwork(N, k)
        self.ActualizeNeighbours()

    def SetLineNetwork(self):
        self.Structure = LineNetwork(self.NumberOfAgents)
        self.ActualizeNeighbours()

    def SumOverNeighbours(self, index, OldGrid):
        Soma = 0
        nearest = self.List[index].Neighbours
        if len(nearest) > 0:
            for i in range(0, len(nearest)):
                Soma = Soma + OldGrid[int(nearest[i])].IsingExpectative
            Soma = self.ImitationRate * Soma / len(nearest)
        else:
            Soma = 0
        return Soma

    def AgentsInovation(self, indice):
        for i in range(0, self.NumberOfAgents):
            self.List[i].Inovation(indice)

    def IsingInteraction(self, Lambda, extMag, indice):
        # inovate
        self.AgentsInovation(indice)
        # interaction
        valor = 0
        OldStates = self.List
        NewStates = self.List
        for i in range(0, self.NumberOfAgents):
            Soma = self.SumOverNeighbours(i, OldStates)
            Magnetization = (extMag*self.OutConversion + self.SelfConversion) * OldStates[i].IsingExpectative + Soma
            prob = np.float(1 / (1 + math.exp(-2 * Magnetization * Lambda)))
            # prob=Magnetization
            alpha = 0
            if OldStates[i].IsingExpectative == 1:
                alpha = min(1, prob)
            else:
                alpha = min(1, 1 - prob)
            if Magnetization <= 0 or np.random.rand() <= alpha:
                NewStates[i].IsingExpectative = -1 * NewStates[i].IsingExpectative
        self.List = NewStates
        valor = sum(a.IsingExpectative for a in self.List) / len(self.List)
        self.Expectative = valor

    def DeGrauweInteraction(self, ro, eyfun, yt, roBH, gamma, indice):
        # inovate all agents
        self.AgentsInovation(indice)
        # agents analyze the situation
        for i in range(0, self.NumberOfAgents):
            self.List[i].ClassificationDeGrauwe(ro, eyfun, yt, roBH, gamma, indice)
        # agents interact
        TotalY = np.zeros((self.NumberOfAgents, 1))
        TotalAlfa = np.zeros((self.NumberOfAgents, 1))
        for i in range(0, self.NumberOfAgents):
            y = np.append(self.List[i].Neighbours, i)
            valuesY = np.zeros((np.size(y), 1))
            valuesAlphaYt = np.zeros((np.size(y), 1))
            for j in range(0, np.size(y)):
                indi = int(y[j])
                valuesY[j] = self.List[indi].OutputGapExpectative
                valuesAlphaYt[j] = self.List[indi].currentAlfaY
            self.List[i].OutputGapExpectative = valuesY[int(np.argmax(valuesAlphaYt))]
            self.List[i].PastOutputGapExpectative[indice] = self.List[i].OutputGapExpectative
            self.List[i].currentAlfaY = np.max((valuesAlphaYt))
            self.List[i].AlfaY[indice] = np.max((valuesAlphaYt))
            TotalY[i] = self.List[i].OutputGapExpectative
            TotalAlfa[i] = np.max(valuesAlphaYt)
        outYt = np.mean(TotalY)
        outAlfaY = np.mean(TotalAlfa)
        out = [outYt, outAlfaY]
        return out