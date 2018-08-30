from NETWORKS import *


class Simulation:
    SimTime = 100
    Grid = None
    Gamma = None
    OutputGapTarget = 0
    #para ising = 15-50
    #para degrauwe= 50-100
    InflationTarget = 0
    ConstantA1 = 0.5
    ConstantA2 = -0.2
    ConstantB1 = 0.5
    ConstantB2 = 0.05
    ConstantC1 = None
    ConstantC2 = None
    ConstantC3 = 0.1
    ConstantSigma1 = 0.5
    ConstantSigma2 = 0.5
    ConstantSigma3 = 0.5
    ConstantRho = 0
    ConstantRhoOut = 0
    ConstantRhoInf = 0
    ConstantRhoTayl = 0
    ConstantRhoBH = 0
    InflationTP = np.zeros((SimTime, 1))
    InflationTPLag = np.zeros((SimTime, 1))
    InterestRateTR = np.zeros((SimTime, 1))
    OutputGapTY = np.zeros((SimTime, 1))
    OutputGapTYLag = np.zeros((SimTime, 1))
    AnimalSpiritsT = np.zeros((SimTime, 1))
    AutoCorrP = None
    AutoCorrY = None
    CorrYS = None
    MeanY = None
    MeanAS = None
    MedianY = None
    MaxY = None
    MinY = None
    MeanP = None
    MedianP = None
    MaxP = None
    MinP = None
    KurtY = None
    JBTY = None
    KurtP = None
    JBTP = None
    StdY = None
    StdP = None
    StdAS = None
    YEntr = None
    PEntr = None

    def __init__(self, tipo, numero, topologia, c11, c22):
        self.Interaction = tipo
        self.SizeOfNetwork = numero
        self.TopologyOfNetwork = topologia
        self.ConstantC1 = c11
        self.ConstantC2 = c22
        self.Grid = Network(numero, tipo, topologia, self.SimTime)
        if self.Interaction is 'Ising':
            self.Gamma = 25
        elif self.Interaction is 'DeGrauwe':
            self.Gamma = 100

    def SetSTDOutputGap(self):
        self.StdY = np.std(self.OutputGapTY)

    def SomeStatisticalTests(self):
        self.StdP = np.std(self.InflationTP)
        self.StdY = np.std(self.OutputGapTY)
        self.StdAS = np.std(self.AnimalSpiritsT)
        self.CorrYS = float(np.correlate(self.OutputGapTY[:, 0], self.AnimalSpiritsT[:, 0]))

    def AllStatisticalTests(self):
        self.AutoCorrP = np.corrcoef(self.InflationTP[:, 0], self.InflationTPLag[:, 0])
        self.AutoCorrY = np.corrcoef(self.OutputGapTY[:, 0], self.OutputGapTYLag[:, 0])
        self.CorrYS = float(np.correlate(self.OutputGapTY[:, 0], self.AnimalSpiritsT[:, 0]))
        self.MeanAS = np.mean(self.AnimalSpiritsT)
        self.MeanY = np.mean(self.OutputGapTY)
        self.MedianY = np.median(self.OutputGapTY)
        self.MaxY = np.amax(self.OutputGapTY)
        self.MinY = np.amin(self.OutputGapTY)
        self.MeanP = np.mean(self.InflationTP)
        self.MedianP = np.median(self.InflationTP)
        self.MaxP = np.amax(self.InflationTP)
        self.MinP = np.amin(self.InflationTP)
        self.KurtY = float(stats.kurtosis(self.OutputGapTY)) #quarto momento estatístico
        self.JBTY = stats.jarque_bera(self.OutputGapTY)
        self.KurtP = float(stats.kurtosis(self.InflationTP)) #quarto momento estatístico
        self.JBTP = stats.jarque_bera(self.InflationTP)
        self.StdP = np.std(self.InflationTP)
        self.StdY = np.std(self.OutputGapTY)
        self.StdAS = np.std(self.AnimalSpiritsT)
        self.YEntr = stats.entropy(self.OutputGapTY)
        self.PEntr = stats.entropy(self.InflationTP)

    def TimeSeriesGraph(self, n):
        tempo = np.arange(0, self.SimTime)
        # plots
        fig1 = plt.figure(1 + n)
        plt.plot(tempo, self.OutputGapTY)
        D1 = pd.Series(self.OutputGapTY[:, 0], tempo)
        d_mva1 = D1.rolling(window=4,center=False).mean()
        plt.plot(tempo,d_mva1)
        plt.ylabel('Output gap')
        plt.xlabel('Time')
        plt.show()
        fig2 = plt.figure(2 + n)
        plt.plot(tempo, self.InflationTP)
        D2 = pd.Series(self.InflationTP[:, 0], tempo)
        d_mva2 = D2.rolling(window=4,center=False).mean()
        plt.plot(tempo, d_mva2)
        plt.ylabel('Inflation')
        plt.xlabel('Time')
        plt.show()
        fig3 = plt.figure(3 + n)
        plt.plot(tempo, self.InterestRateTR)
        D3 = pd.Series(self.InterestRateTR[:, 0], tempo)
        d_mva3 = D3 .rolling(window=4,center=False).mean()
        plt.plot(tempo, d_mva3)
        plt.ylabel('Interest rate')
        plt.xlabel('Time')
        plt.show()
        fig4 = plt.figure(4 + n)
        plt.plot(tempo, self.AnimalSpiritsT)
        plt.ylabel('Animal spirits')
        plt.xlabel('Time')
        plt.show()

    def ChangeSimulationTime(self, novoTempo):
        self.SimTime = novoTempo
        self.InflationTP = np.zeros((self.SimTime, 1))
        self.InflationTPLag = np.zeros((self.SimTime, 1))
        self.InterestRateTR = np.zeros((self.SimTime, 1))
        self.OutputGapTY = np.zeros((self.SimTime, 1))
        self.OutputGapTYLag = np.zeros((self.SimTime, 1))
        self.AnimalSpiritsT = np.zeros((self.SimTime, 1))
        self.Grid = Network(self.SizeOfNetwork, self.Interaction, self.TopologyOfNetwork, self.SimTime)

    def MakeSimulation(self):
        if self.Interaction is 'Ising':
            self.IsingAntBasedSimulation()
        elif self.Interaction is 'DeGrauwe':
            self.DeGrauweSimulation()
    def SaveSimulationFigures(self, nbins):
        n = 0
        tempo = np.arange(0, self.SimTime)
        fig1 = plt.figure(1 + n)
        plt.plot(tempo, self.OutputGapTY)
        D1 = pd.Series(self.OutputGapTY[:, 0], tempo)
        d_mva1 = D1.rolling(window=4, center=False).mean()
        plt.plot(tempo, d_mva1)
        plt.ylabel('Output gap')
        plt.xlabel('Time')
        fig2 = plt.figure(2 + n)
        plt.plot(tempo, self.InflationTP)
        D2 = pd.Series(self.InflationTP[:, 0], tempo)
        d_mva2 = D2.rolling(window=4,center=False).mean()
        plt.plot(tempo, d_mva2)
        plt.ylabel('Inflation')
        plt.xlabel('Time')
        fig3 = plt.figure(3 + n)
        plt.plot(tempo, self.InterestRateTR)
        D3 = pd.Series(self.InterestRateTR[:, 0], tempo)
        d_mva3 = D3 .rolling(window=4,center=False).mean()
        plt.plot(tempo, d_mva3)
        plt.ylabel('Interest rate')
        plt.xlabel('Time')
        fig4 = plt.figure(4 + n)
        plt.plot(tempo, self.AnimalSpiritsT)
        plt.ylabel('Animal spirits')
        plt.xlabel('Time')
        fig5 = plt.figure(5 + n)
        plt.hist(self.OutputGapTY, nbins)
        plt.title('Output Gap frequency distribution in one cycle')
        fig6 = plt.figure(6 + n)
        plt.hist(self.InflationTP, nbins)
        plt.title('Inflation frequency distribution in one cycle')
        fig7 = plt.figure(7 + n)
        plt.hist(self.InterestRateTR, nbins)
        plt.title('Interest rate frequency distribution in one cycle')
        fig8 = plt.figure(8 + n)
        plt.hist(self.AnimalSpiritsT, nbins)
        plt.title('Animal spirits frequency distribution in one cycle')
        now = datetime.datetime.now()
        nome = 'Hora' + str(now.hour) + 'Dia' + str(now.day) + 'Mes' + str(now.month) + 'Ano' + str(
            now.year) + self.Grid.TypeOfInteraction + self.Grid.Topology
        nome1 = nome + 'OutputGapTime' + '.png'
        fig1.savefig(nome1)
        nome2 = nome + 'InflationTime' + '.png'
        fig2.savefig(nome2)
        nome3 = nome + 'InterestRateTime' + '.png'
        fig3.savefig(nome3)
        nome4 = nome + 'AnimalSpiritsTime' + '.png'
        fig4.savefig(nome4)
        nome5 = nome + 'OutputGapFreq' + '.png'
        fig5.savefig(nome5)
        nome6 = nome + 'InflationFreq' + '.png'
        fig6.savefig(nome6)
        nome7 = nome + 'InterestRateFreq' + '.png'
        fig7.savefig(nome7)
        nome8 = nome + 'AnimalSpiritsFreq' + '.png'
        fig8.savefig(nome8)

    def FrequencyGraphOfTimeSeries(self, n, nbins):
        # plots
        fig1 = plt.figure(1 + n)
        MakeAnHistogram(self.OutputGapTY, 'Output Gap frequency distribution in one cycle', nbins)
        fig2 = plt.figure(2 + n)
        MakeAnHistogram(self.InflationTP, 'Inflation frequency distribution in one cycle', nbins)
        fig3 = plt.figure(3 + n)
        MakeAnHistogram(self.InterestRateTR, 'Interest rate frequency distribution in one cycle', nbins)
        fig4 = plt.figure(4 + n)
        MakeAnHistogram(self.AnimalSpiritsT, 'Animal spirits frequency distribution in one cycle', nbins)

    def IsingAntBasedSimulation(self):
        #print('IsingAntBasedSimulation')
        A = np.matrix(
            [[1, -self.ConstantB2], [-self.ConstantA2 * self.ConstantC1, 1 - self.ConstantA2 * self.ConstantC2]])
        B = np.matrix([[self.ConstantB1, 0], [-self.ConstantA2, self.ConstantA1]])
        C = np.matrix([[1 - self.ConstantB1, 0], [0, 1 - self.ConstantA1]])
        p = np.zeros((self.SimTime, 1))
        y = np.zeros((self.SimTime, 1))
        plagt = np.zeros((self.SimTime, 1))
        ylagt = np.zeros((self.SimTime, 1))
        r = np.zeros((self.SimTime, 1))
        eyfunt = np.zeros((self.SimTime, 1))
        CRy = np.zeros((self.SimTime, 1))
        FRy = np.zeros((self.SimTime, 1))
        alfayt = np.zeros((self.SimTime, 1))
        anspirits = np.zeros((self.SimTime, 1))
        epsilont = np.zeros((self.SimTime, 1))
        etat = np.zeros((self.SimTime, 1))
        ut = np.zeros((self.SimTime, 1))
        #################################################
        # heuristic model
        #################################################
        alfay = 0.5
        alfayt[0] = alfay
        anspirits[0] = alfay
        for t in range(1, self.SimTime):
            epsilont[t] = self.ConstantRhoOut * epsilont[
                t - 1] + self.ConstantSigma1 * np.random.randn()  # shocks in output equation (demand shock)
            etat[t] = self.ConstantRhoInf * etat[
                t - 1] + self.ConstantSigma2 * np.random.randn()  # shocks in inflation equation (supply shock)
            ut[t] = self.ConstantRhoTayl * ut[
                t - 1] + self.ConstantSigma3 * np.random.randn()  # shocks in Taylor rule (interest rate shock)
            epsilon = epsilont[t]
            eta = etat[t]
            u = ut[t]
            shocks = np.array([eta, self.ConstantA2 * u + epsilon])
            eps = self.InflationTarget +np.random.randn()*((self.ConstantSigma1+self.ConstantSigma2+self.ConstantSigma3)/3)
            eyfun = self.OutputGapTarget+np.random.randn()*((self.ConstantSigma1+self.ConstantSigma2+self.ConstantSigma3)/3)
            eychar = y[t - 1]
            eyfunt[t] = eyfun
            eys = alfay * eychar + (1 - alfay) * eyfun
            forecast = np.array([eps, eys])
            plag = p[t - 1]
            ylag = y[t - 1]
            rlag = r[t - 1]
            lag = np.array([plag, ylag])
            smooth = np.array([0, self.ConstantA2 * self.ConstantC3])
            D = B.dot(forecast).reshape((-1, 1)) + C.dot(lag).reshape((-1, 1)) + rlag * smooth.reshape(
                (-1, 1)) + shocks.reshape((-1, 1))
            X = linalg.solve(A, D)
            p[t] = X[0]
            y[t] = X[1]
            r[t] = self.ConstantC1 * p[t] + self.ConstantC2 * y[t] + self.ConstantC3 * r[t - 1] + u
            plagt[t] = p[t - 1]
            ylagt[t] = y[t - 1]
            CRy[t] = self.ConstantRho * CRy[t - 1] - (1 - self.ConstantRho) * (eychar - y[t]) ** 2
            FRy[t] = self.ConstantRho * FRy[t - 1] - (1 - self.ConstantRho) * (eyfun - y[t]) ** 2
            try:
                exponencialCRy = math.exp(self.Gamma * CRy[t])
            except OverflowError:
                exponencialCRy = float('inf')
            try:
                exponencialFRy = math.exp(self.Gamma * FRy[t])
            except OverflowError:
                exponencialFRy = float('inf')
            alfay = self.ConstantRhoBH * alfayt[t - 1] + (1 - self.ConstantRhoBH) * exponencialCRy / (
                    exponencialCRy + exponencialFRy)
            if math.isnan(alfay):
                alfay=1
            elif alfay>1:
                alfay=1
            elif alfay<0:
                alfay=0
            ExtMagIn = 2 * alfay - 1
            self.Grid.IsingInteraction(self.Gamma, ExtMagIn, t)
            alfay = 0.5 * self.Grid.Expectative + 0.5
            alfayt[t] = alfay
            if eychar > 0:
                anspirits[t] = alfay
            if eychar < 0:
                anspirits[t] = 1 - alfay
        self.OutputGapTY = y
        self.OutputGapTYLag = ylagt
        self.InterestRateTR = r
        self.InflationTP = p
        self.InflationTPLag = plagt
        self.AnimalSpiritsT = 2.0 * (anspirits - 0.5)

    def DeGrauweSimulation(self):
        #print('DeGrauweSimulation')
        A = np.matrix(
            [[1, -self.ConstantB2], [-self.ConstantA2 * self.ConstantC1, 1 - self.ConstantA2 * self.ConstantC2]])
        B = np.matrix([[self.ConstantB1, 0], [-self.ConstantA2, self.ConstantA1]])
        C = np.matrix([[1 - self.ConstantB1, 0], [0, 1 - self.ConstantA1]])
        p = np.zeros((self.SimTime, 1))
        y = np.zeros((self.SimTime, 1))
        plagt = np.zeros((self.SimTime, 1))
        ylagt = np.zeros((self.SimTime, 1))
        r = np.zeros((self.SimTime, 1))
        eyfunt = np.zeros((self.SimTime, 1))
        alfayt = np.zeros((self.SimTime, 1))
        anspirits = np.zeros((self.SimTime, 1))
        epsilont = np.zeros((self.SimTime, 1))
        etat = np.zeros((self.SimTime, 1))
        ut = np.zeros((self.SimTime, 1))
        #################################################
        # heuristic model
        #################################################
        yt=y[0]
        eyfun = self.OutputGapTarget + np.random.randn() * ((self.ConstantSigma1 + self.ConstantSigma2 + self.ConstantSigma3) / 3)
        anspirits[0] = 0.5
        alfayAG = []
        eys = self.Grid.FirstDeGrauweExpectative(self.ConstantRho, eyfun, yt, self.ConstantRhoBH,
                                                               self.Gamma, 0)
        for t in range(1, self.SimTime):
            epsilont[t] = self.ConstantRhoOut * epsilont[
                t - 1] + self.ConstantSigma1 * np.random.randn()  # shocks in output equation (demand shock)
            etat[t] = self.ConstantRhoInf * etat[
                t - 1] + self.ConstantSigma2 * np.random.randn()  # shocks in inflation equation (supply shock)
            ut[t] = self.ConstantRhoTayl * ut[
                t - 1] + self.ConstantSigma3 * np.random.randn()  # shocks in Taylor rule (interest rate shock)
            epsilon = epsilont[t]
            eta = etat[t]
            u = ut[t]
            shocks = np.array([eta, self.ConstantA2 * u + epsilon])
            eps = self.InflationTarget+np.random.randn()*((self.ConstantSigma1+self.ConstantSigma2+self.ConstantSigma3)/3)
            eyfun = self.OutputGapTarget+np.random.randn()*((self.ConstantSigma1+self.ConstantSigma2+self.ConstantSigma3)/3)
            eyfunt[t] = eyfun
            if t >1:
                eys = np.mean(eysAG)
            forecast = np.array([eps, eys])
            plag = p[t - 1]
            ylag = y[t - 1]
            rlag = r[t - 1]
            lag = np.array([plag, ylag])
            smooth = np.array([0, self.ConstantA2 * self.ConstantC3])
            D = B.dot(forecast).reshape((-1, 1)) + C.dot(lag).reshape((-1, 1)) + rlag * smooth.reshape(
                (-1, 1)) + shocks.reshape((-1, 1))
            X = linalg.solve(A, D)
            p[t] = X[0]
            y[t] = X[1]
            yt = X[1]
            r[t] = self.ConstantC1 * p[t] + self.ConstantC2 * y[t] + self.ConstantC3 * r[t - 1] + u
            plagt[t] = p[t - 1]
            ylagt[t] = y[t - 1]
            eycharAG, alfayAG, eysAG  = self.Grid.DeGrauweInteraction(self.ConstantRho, eyfun, yt, self.ConstantRhoBH,
                                                               self.Gamma, t)
            alfay = np.mean(alfayAG)
            alfayt[t] = alfay
            eychar=np.mean(eycharAG)
            if eychar > 0:
                anspirits[t] = alfay
            if eychar < 0:
                anspirits[t] = 1 - alfay
        self.OutputGapTY = y
        self.OutputGapTYLag = ylagt
        self.InterestRateTR = r
        self.InflationTP = p
        self.InflationTPLag = plagt
        self.AnimalSpiritsT = 2.0 * (anspirits - 0.5)
