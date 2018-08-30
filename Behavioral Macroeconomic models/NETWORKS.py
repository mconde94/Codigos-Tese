from AGENTS import *


class Network:
    NumberOfAgents = None
    Topology = None
    CircularOrder = 2
    RandomNeighbours = 10
    Structure = None
    List = []
    SelfConversion = 0.15  # self-conversion rate on the Ising Model
    ImitationRate = 0.6  # imititation rate on the Ising Model
    OutConversion = 0.3
    Expectative = None
    CentralBank = None

    def __init__(self, n, interaction, t, tempo):
        self.NumberOfAgents = n
        self.Topology = t
        self.List = 2 * np.zeros(self.NumberOfAgents, dtype=Agent)
        if interaction is not 'Ising':
            self.CentralBank = Agent(interaction,tempo)
            self.CentralBank.OutputGapExpectative = 0
            self.CentralBank.PastOutputGapExpectative[0] = self.CentralBank.OutputGapExpectative
        for i in range(0, self.NumberOfAgents):
            self.List[i] = Agent(interaction, tempo)
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
        elif self.Topology is 'AmericaC':
            self.SetAmericanConnectedNetwork()
        elif self.Topology is 'MexicoC':
            self.SetMexicanConnectedNetwork()
        elif self.Topology is 'EuropeC':
            self.SetEuropeanConnectedNetwork()
        elif self.Topology is 'BrazilC':
            self.SetBrazilConnectedNetwork()
        elif self.Topology is 'AmericaS':
            self.SetAmericanSeparatedNetwork()
        elif self.Topology is 'EuropeS':
            self.SetEuropeanSeparatedNetwork()
        elif self.Topology is 'BrazilS':
            self.SetBrazilSeparatedNetwork()
        elif self.Topology is 'MexicanS':
            self.SetMexicanSeparatedNetwork()

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

    def SetEuropeanConnectedNetwork(self):
        self.Structure = ConnectedEuropeanNetwork()
        self.ActualizeNeighbours()

    def SetEuropeanSeparatedNetwork(self):
        self.Structure = SeparatedEuropeanNetwork()
        self.ActualizeNeighbours()

    def SetBrazilConnectedNetwork(self):
        self.Structure = ConnectedBrazilNetwork()
        self.ActualizeNeighbours()

    def SetBrazilSeparatedNetwork(self):
        self.Structure = SeparatedBrazilNetwork()
        self.ActualizeNeighbours()

    def SetAmericanConnectedNetwork(self):
        self.Structure = ConnectedAmericanNetwork()
        self.ActualizeNeighbours()

    def SetAmericanSeparatedNetwork(self):
        self.Structure = SeparatedAmericanNetwork()
        self.ActualizeNeighbours()

    def SetMexicanConnectedNetwork(self):
        self.Structure = ConnectedMexicanNetwork()
        self.ActualizeNeighbours()

    def SetMexicanSeparatedNetwork(self):
        self.Structure = SeparatedMexicanNetwork()
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
        flag = False
        if self.List[index].ProbabilityOfInovation > np.random.rand():
            flag = True
        if len(nearest) > 0:
            for i in range(0, len(nearest)):
                Soma = Soma + OldGrid[int(nearest[i])].IsingExpectative
            if flag == True:
                Soma = Soma + 2 * np.random.randint(2) - 1
                Soma = self.ImitationRate * Soma / (len(nearest)+1)
            else:
                Soma = self.ImitationRate * Soma / len(nearest)
        else:
            Soma = 0
        return Soma

    def FirstDeGrauweExpectative(self, ro, eyfun, yt, roBH, gamma, indice):
        for i in range(0, self.NumberOfAgents):
            self.List[i].ClassificationDeGrauwe(ro, eyfun, yt, roBH, gamma, indice)
        EYS = np.zeros((self.NumberOfAgents,1))
        for i in range(0,self.NumberOfAgents):
            EYS[i] = self.List[i].currentAlfaY*self.List[i].OutputGapExpectative+(1-self.List[i].currentAlfaY)*eyfun
        outEYS = np.mean(EYS)
        return outEYS

    def DeGrauweInteraction(self, ro, eyfun, yt, roBH, gamma, indice):
        # inovate all agents
        OldNetwork = self
        # agents analyze the situation
        for i in range(0, self.NumberOfAgents):
            OldNetwork.List[i].ClassificationDeGrauwe(ro, eyfun, yt, roBH, gamma, indice)
        # agents interact
        FinalY = np.zeros((self.NumberOfAgents, 1))
        FinalAlfa = np.zeros((self.NumberOfAgents, 1))
        FinalEys = np.zeros((self.NumberOfAgents,1))
        for i in range(0, self.NumberOfAgents):
            Inovation = False
            vizinhos =  OldNetwork.List[i].Neighbours
            newAgent = []
            if OldNetwork.List[i].ProbabilityOfInovation > np.random.rand():
                newAgent = Agent(OldNetwork.List[i].TypeOfAgent,OldNetwork.List[i].TotalTime)
                newAgent.DeGrauweInovation(indice)
                newAgent.ClassificationDeGrauwe(ro, eyfun, yt, roBH, gamma, indice)
                Inovation = True
            vizinhos = np.append(vizinhos, i)
            valuesY = np.zeros((np.size(vizinhos), 1))
            valuesAlphaYt = np.zeros((np.size(vizinhos), 1))
            for j in range(0, np.size(vizinhos)):
                indi = int(vizinhos[j])
                valuesY[j] = OldNetwork.List[indi].OutputGapExpectative
                valuesAlphaYt[j] = OldNetwork.List[indi].currentAlfaY
            if Inovation == True:
                valuesY = np.append(valuesY,newAgent.OutputGapExpectative)
                valuesAlphaYt = np.append(valuesAlphaYt, newAgent.currentAlfaY)
            self.List[i].OutputGapExpectative = valuesY[int(np.argmax(valuesAlphaYt))]
            self.List[i].PastOutputGapExpectative[indice] = valuesY[int(np.argmax(valuesAlphaYt))]
            self.List[i].currentAlfaY = np.max((valuesAlphaYt))
            self.List[i].AlfaY[indice] = np.max((valuesAlphaYt))
            FinalY[i] = self.List[i].OutputGapExpectative
            FinalAlfa[i] = np.max(valuesAlphaYt)
            #print(FinalAlfa[i])
            if FinalAlfa[i]>0.5:
                FinalEys[i] = FinalY[i]
            else:
                FinalEys[i] = eyfun
                FinalAlfa[i] = 0
                self.List[i].OutputGapExpectative = eyfun
                self.List[i].PastOutputGapExpectative[indice] = eyfun
                self.List[i].currentAlfaY = 0
                self.List[i].AlfaY[indice] = 0
        return FinalY, FinalAlfa , FinalEys

    def IsingInteraction(self, Lambda, extMag, indice):
        OldStates = self.List
        NewStates = self.List
        for i in range(0, self.NumberOfAgents):
            Soma = self.SumOverNeighbours(i, OldStates)
            Magnetization = (extMag*self.OutConversion + self.SelfConversion) * OldStates[i].IsingExpectative + Soma
            miolo = -2* Magnetization * Lambda
            try:
                exponencial = math.exp(miolo)
            except OverflowError:
                exponencial = float('inf')
            prob = np.float(1 / (1 + exponencial))
            if OldStates[i].IsingExpectative == 1:
                alpha = min(1, prob)
            else:
                alpha = min(1, 1 - prob)
            if Magnetization <= 0 or np.random.rand() <= alpha:
                NewStates[i].IsingExpectative = -1 * NewStates[i].IsingExpectative
            self.List[i].PastIsingExpectative[indice] = NewStates[i].IsingExpectative
        self.List = NewStates
        valor = sum(a.IsingExpectative for a in self.List) / len(self.List)
        self.Expectative = valor
