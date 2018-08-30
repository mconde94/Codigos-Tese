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
    IsingExpectative = None
    OutputGapExpectative = None
    PastIsingExpectative = None
    PastOutputGapExpectative = None
    Neighbours = []
    Score = None

    def __init__(self, AgenteTipo, t):
        self.TypeOfAgent = AgenteTipo
        self.TotalTime = t
        if self.TypeOfAgent is 'Ising':
            self.PastIsingExpectative = np.zeros((self.TotalTime, 1))
            self.IsingExpectative = 2 * np.random.randint(2) - 1
            self.PastIsingExpectative[0] = self.IsingExpectative
        else:
            self.yCR = np.zeros((self.TotalTime, 1))
            self.yFR = np.zeros((self.TotalTime, 1))
            self.currentAlfaY = np.random.rand( )
            self.AlfaY = np.zeros((self.TotalTime, 1))
            self.AlfaY[0] = self.currentAlfaY
            self.PastOutputGapExpectative = np.zeros((self.TotalTime, 1))
            self.OutputGapExpectative = (np.random.randint(self.lowest, high=self.highest) +  np.random.rand())*0.1*5
            self.PastOutputGapExpectative[0] = self.OutputGapExpectative

    def DeGrauweInovation(self, indice):
        if self.TypeOfAgent is not 'Ising':
            flag=(np.random.randint(self.lowest, high=self.highest) + np.random.rand())*0.1
            self.OutputGapExpectative = flag
            self.PastOutputGapExpectative[indice] = flag


    def ClassificationDeGrauwe(self, ro, eyfun, yt, roBH, gamma, indice):
        if indice>0:
            CRynew = ro * self.yCR[indice - 1] - (1 - ro) * (self.OutputGapExpectative - yt) ** 2
            self.yCR[indice] = CRynew
            FRynew = ro * self.yFR[indice - 1] - (1 - ro) * (eyfun - yt) ** 2
            self.yFR[indice] = FRynew
        else:
            CRynew = (1 - ro) * (self.OutputGapExpectative - yt) ** 2
            self.yCR[indice] =  CRynew
            FRynew = (1 - ro) * (eyfun - yt) ** 2
            self.yFR[indice] = FRynew
        min = 2.2250738585072014e-308
        denominador = math.exp(gamma * self.yCR[np.size(self.yCR) - 1]) + math.exp(
            gamma * self.yFR[np.size(self.yCR) - 1])
        # seguranca para nao haver
        if denominador <= min*10:
            denominador = min*10
        self.currentAlfaY = roBH * self.currentAlfaY + (1 - roBH) * math.exp(
            gamma * self.yCR[np.size(self.yCR) - 1]) / denominador
        self.AlfaY[indice] = self.currentAlfaY
