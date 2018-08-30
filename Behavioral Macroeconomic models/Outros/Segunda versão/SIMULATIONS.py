from NETWORKS import *


class Simulation:
    Time = 100
    Grid = None
    Gamma = 10
    InflationTarget = 0
    ConstantA1 = 0.5
    ConstantA2 = -0.2
    ConstantB1 = 0.5
    ConstantB2 = 0.05
    ConstantC1 = None
    ConstantC2 = None
    ConstantC3 = 0.5
    ConstantSigma1 = 0.5
    ConstantSigma2 = 0.5
    ConstantSigma3 = 0.5
    ConstantRho = 0
    ConstantRhoOut = 0
    ConstantRhoInf = 0
    ConstantRhoTayl = 0
    ConstantRhoBH = 0
    InflationTP = np.zeros((Time, 1))
    InflationTPLag = np.zeros((Time, 1))
    InterestRateTR = np.zeros((Time, 1))
    OutputGapTY = np.zeros((Time, 1))
    OutputGapTYLag = np.zeros((Time, 1))
    AnimalSpiritsT = np.zeros((Time, 1))
    AutoCorrP = None
    AutoCorrY = None
    CorrYS = None
    MeanY = None
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
    YEntr = None
    PEntr = None

    def __init__(self, tipo, numero, topologia, c11, c22):
        self.Interaction = tipo
        self.SizeOfNetwork = numero
        self.TopologyOfNetwork = topologia
        self.ConstantC1 = c11
        self.ConstantC2 = c22
        self.Grid = Network(numero, tipo, topologia, self.Time)

    def SetSTDOutputGap(self):
        self.StdY = np.std(self.OutputGapTY)

    def AllStatisticalTests(self):
        self.AutoCorrP = np.corrcoef(self.InflationTP[:, 0], self.InflationTPLag[:, 0])
        self.AutoCorrY = np.corrcoef(self.OutputGapTY[:, 0], self.OutputGapTYLag[:, 0])
        self.CorrYS = np.correlate(self.OutputGapTY[:, 0], self.AnimalSpiritsT[:, 0])
        self.MeanY = np.mean(self.OutputGapTY)
        self.MedianY = np.median(self.OutputGapTY)
        self.MaxY = np.amax(self.OutputGapTY)
        self.MinY = np.amin(self.OutputGapTY)
        self.MeanP = np.mean(self.InflationTP)
        self.MedianP = np.median(self.InflationTP)
        self.MaxP = np.amax(self.InflationTP)
        self.MinP = np.amin(self.InflationTP)
        self.KurtY = stats.kurtosis(self.OutputGapTY)
        self.JBTY = stats.jarque_bera(self.OutputGapTY)
        self.KurtP = stats.kurtosis(self.InflationTP)
        self.JBTP = stats.jarque_bera(self.InflationTP)
        self.StdP = np.std(self.InflationTP)
        self.StdY = np.std(self.OutputGapTY)
        self.YEntr = stats.entropy(self.OutputGapTY)
        self.PEntr = stats.entropy(self.InflationTP)

    def TimeSeriesGraph(self, n):
        tempo = np.arange(0, self.Time)
        # plots
        fig1 = plt.figure(1 + n)
        plt.plot(tempo, self.OutputGapTY)
        plt.ylabel('output gap')
        plt.xlabel('time')
        plt.show()
        fig2 = plt.figure(2 + n)
        plt.plot(tempo, self.InflationTP)
        plt.ylabel('inflation')
        plt.xlabel('time')
        plt.show()
        fig3 = plt.figure(3 + n)
        plt.plot(tempo, self.InterestRateTR)
        plt.ylabel('interest rate')
        plt.xlabel('time')
        plt.show()
        fig4 = plt.figure(4 + n)
        plt.plot(tempo, self.AnimalSpiritsT)
        plt.ylabel('animal spirits')
        plt.xlabel('time')
        plt.show()

    def FrequencyGraphOfTimeSeries(self, n):
        # plots
        fig1 = plt.figure(1 + n)
        MakeAnHistogram(self.OutputGapTY, 'Output Gap frequency distribution in a cycle', 50)
        fig2 = plt.figure(2 + n)
        MakeAnHistogram(self.InflationTP, 'Inflation frequency distribution in a cycle', 50)
        fig3 = plt.figure(3 + n)
        MakeAnHistogram(self.InterestRateTR, 'Interest rate frequency distribution in a cycle', 50)
        fig4 = plt.figure(4 + n)
        MakeAnHistogram(self.AnimalSpiritsT, 'Animal spirits frequency distribution in a cycle', 50)

    def IsingAntBasedSimulation(self):
        A = np.matrix([[1, -self.ConstantB2], [-self.ConstantA2 * self.ConstantC1, 1 - self.ConstantA2 * self.ConstantC2]])
        B = np.matrix([[self.ConstantB1, 0], [-self.ConstantA2, self.ConstantA1]])
        C = np.matrix([[1 - self.ConstantB1, 0], [0, 1 - self.ConstantA1]])
        p = np.zeros((self.Time, 1))
        y = np.zeros((self.Time, 1))
        plagt = np.zeros((self.Time, 1))
        ylagt = np.zeros((self.Time, 1))
        r = np.zeros((self.Time, 1))
        eyfunt = np.zeros((self.Time, 1))
        CRy = np.zeros((self.Time, 1))
        FRy = np.zeros((self.Time, 1))
        alfayt = np.zeros((self.Time, 1))
        anspirits = np.zeros((self.Time, 1))
        epsilont = np.zeros((self.Time, 1))
        etat = np.zeros((self.Time, 1))
        ut = np.zeros((self.Time, 1))
        #################################################
        # heuristic model
        #################################################
        alfay = 0.5
        alfayt[0] = alfay
        anspirits[0]=alfay
        for t in range(1, self.Time):
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
            eps = self.InflationTarget
            eyfun = np.random.randn() / 2
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
            alfay = self.ConstantRhoBH * alfayt[t - 1] + (1 - self.ConstantRhoBH) * math.exp(self.Gamma * CRy[t]) / (
                        math.exp(self.Gamma * CRy[t]) + math.exp(self.Gamma * FRy[t]))
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
        self.AnimalSpiritsT = anspirits-0.5

    def DeGrauweSimulation(self):
        A = np.matrix(
            [[1, -self.ConstantB2], [-self.ConstantA2 * self.ConstantC1, 1 - self.ConstantA2 * self.ConstantC2]])
        B = np.matrix([[self.ConstantB1, 0], [-self.ConstantA2, self.ConstantA1]])
        C = np.matrix([[1 - self.ConstantB1, 0], [0, 1 - self.ConstantA1]])
        p = np.zeros((self.Time, 1))
        y = np.zeros((self.Time, 1))
        plagt = np.zeros((self.Time, 1))
        ylagt = np.zeros((self.Time, 1))
        r = np.zeros((self.Time, 1))
        eyfunt = np.zeros((self.Time, 1))
        alfayt = np.zeros((self.Time, 1))
        anspirits = np.zeros((self.Time, 1))
        epsilont = np.zeros((self.Time, 1))
        etat = np.zeros((self.Time, 1))
        ut = np.zeros((self.Time, 1))
        #################################################
        # heuristic model
        #################################################
        alfay = 0.5
        eychar = 0
        for t in range(1, self.Time):
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
            eps = self.InflationTarget
            eyfun = np.random.randn() / 2
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
            yt = X[1]
            r[t] = self.ConstantC1 * p[t] + self.ConstantC2 * y[t] + self.ConstantC3 * r[t - 1] + u
            plagt[t] = p[t - 1]
            ylagt[t] = y[t - 1]
            inter = self.Grid.DeGrauweInteraction(self.ConstantRho, eyfun, yt, self.ConstantRhoBH, self.Gamma, t)
            alfay = inter[0]
            eychar = inter[1]
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
        self.AnimalSpiritsT = anspirits