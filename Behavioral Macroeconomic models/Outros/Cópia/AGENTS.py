from OTHERS import *

class Agent:
    TypeOfAgent=None
    ProbabilityOfInovation=0.05
    yCR=np.array([0])
    yFR=np.array([0])
    AlfaY=np.array([0.5])
    currentAlfaY=0.5
    lowest=-3
    highest=2
    IsingExpectative=2*np.random.randint(2)-1
    OutputGapExpectative=np.random.randint(lowest,high= highest)+np.random.rand()
    PastIsingExpectative=np.array([IsingExpectative])
    PastOutputGapExpectative=np.array([OutputGapExpectative])
    Neighbours=[]
    Score=None
    def __init__(self,AgenteTipo):
        self.TypeOfAgent=AgenteTipo
    def Inovation(self):
        if np.random.rand()>self.ProbabilityOfInovation:
            if self.TypeOfAgent is 'Ising':
                self.IsingExpectative=2*np.random.randint(2)-1
                self.PastIsingExpectative[len(self.PastIsingExpectative) -1]=self.IsingExpectative
            else:
                self.OutputGapExpectative=np.random.randint(self.lowest,high=self.highest)+np.random.rand()
                self.PastOutputGapExpectative[len(self.PastOutputGapExpectative) -1]=self.OutputGapExpectative
    def ClassificationDeGrauwe(self,ro,eyfun,yt,roBH,gamma):
        CRynew=ro*self.yCR[np.size(self.yCR)-1]-(1-ro)*(self.OutputGapExpectative-yt)**2
        self.yCR=np.append(self.yCR,CRynew)
        FRynew=ro*self.yFR[np.size(self.yFR)-1]-(1-ro)*(eyfun-yt)**2
        self.yFR=np.append(self.yFR,FRynew)
        self.currentAlfaY=roBH*self.currentAlfaY+(1-roBH)*math.exp(gamma*self.yCR[np.size(self.yCR)-1])/(math.exp(gamma*self.yCR[np.size(self.yCR)-1]) + math.exp(gamma * self.yFR[np.size(self.yCR)-1]))
        self.AlfaY=np.append(self.AlfaY,self.currentAlfaY)