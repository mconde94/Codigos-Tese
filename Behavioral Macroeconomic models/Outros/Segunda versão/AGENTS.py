from OTHERS import *


class Agent:
    TypeOfAgent = None
    TotalTime = None
    ProbabilityOfInovation = 0.05
    yCR = None
    yFR = None
    AlfaY = None
    currentAlfaY = None
    lowest = -3
    highest = 2
    IsingExpectative = 2 * np.random.randint(2) - 1
    OutputGapExpectative = np.random.randint(lowest, high=highest) + np.random.rand()
    PastIsingExpectative = None
    PastOutputGapExpectative = None
    Neighbours = []
    Score = None

    def __init__(self, AgenteTipo, t):
        self.TypeOfAgent = AgenteTipo
        self.TotalTime = t
        if self.TypeOfAgent is 'Ising':
            self.PastIsingExpectative = np.zeros((self.TotalTime, 1))
            self.PastIsingExpectative[0] = self.IsingExpectative
        else:
            self.yCR = np.zeros((self.TotalTime, 1))
            self.yFR = np.zeros((self.TotalTime, 1))
            self.currentAlfaY = 0.5
            self.AlfaY = np.zeros((self.TotalTime, 1))
            self.AlfaY[0] = self.currentAlfaY
            self.PastOutputGapExpectative = np.zeros((self.TotalTime, 1))
            self.PastOutputGapExpectative[0] = self.OutputGapExpectative

    def Inovation(self, indice):
        if np.random.rand() > self.ProbabilityOfInovation:
            if self.TypeOfAgent is 'Ising':
                flag=2 * np.random.randint(2) - 1
                self.IsingExpectative = flag
                self.PastIsingExpectative[indice] = flag
            else:
                flag=np.random.randint(self.lowest, high=self.highest) + np.random.rand()
                self.OutputGapExpectative = flag
                self.PastOutputGapExpectative[indice] = flag

    def ClassificationDeGrauwe(self, ro, eyfun, yt, roBH, gamma, indice):
        CRynew = ro * self.yCR[np.size(self.yCR) - 1] - (1 - ro) * (self.OutputGapExpectative - yt) ** 2
        self.yCR[indice] = CRynew
        FRynew = ro * self.yFR[np.size(self.yFR) - 1] - (1 - ro) * (eyfun - yt) ** 2
        self.yFR[indice] = FRynew
        self.currentAlfaY = roBH * self.currentAlfaY + (1 - roBH) * math.exp(
            gamma * self.yCR[np.size(self.yCR) - 1]) / (math.exp(gamma * self.yCR[np.size(self.yCR) - 1]) + math.exp(
            gamma * self.yFR[np.size(self.yCR) - 1]))
        self.AlfaY[indice] = self.currentAlfaY
