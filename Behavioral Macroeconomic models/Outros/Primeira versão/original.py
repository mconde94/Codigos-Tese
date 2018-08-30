from __future__ import division
import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt	
import math as math
from scipy.stats import stats
from scipy.optimize import nnls
from scipy import linalg


#parametros do modelo
gama = 1 #parametro de mudanca gama no modelo de Brock Hommes
InflacaoDesejada = 2 #inflacao desejada do banco central
epRacional=0 #previsao racional da inflacao (=1)
epExtrapolacao=0 #previsao extrapolativa da inflacao (=1)
a1 = 0.5 #coeficiente do output esperado na eq do output gap
a2 = -0.0 #elasticidade da taxa de juro na eq do output gap
b1 = 0.5#coeficiente da inflacao esperada na eq da inflacao
b2 = 0.05 #coeficiente de output na eq da inflacao
c1 = 1.5 #coeficiente da inflacao na eq de Taylor
c2 = 0.5 #coeficiente do outputgap na eq de Taylor
c3 = 0.5 #parametro de suavidade da taxa de juro eq de Taylor
A = np.matrix('1 -b2;-a2*c1 1-a2*c2')
B = np.matrix('b1 0;-a2 a1')
C = np.matrix('1-b1 0;0 1-a1')
T = 200
sigma1 = 0.5   #desvio padrao choque da eq do output gap
sigma2 = 0.5   #desvio padrao choque da eq da inflacao
sigma3 = 0.5   #desvio padrao choque da eq de Taylor
ro=0.5   #ro na media dos erros quadrados
roOut=0.0   #ro nos choques na eq do output gap
roInf=0.0   #ro nos choques na eq da inflacao
roTayl=0.0   #ro nos choques na equacao de Taylor
roBH=0.0   #ro do modelo de Brock Homes
epfs=InflacaoDesejada   #inflacao esperada alvo
p = np.zeros(T)
y = np.zeros(T)
plagt = np.zeros(T)
ylagt = np.zeros(T)
r = np.zeros(T)
epf = np.zeros(T)
epc = np.zeros(T)
ep = np.zeros(T)
ey = np.zeros(T)
CRp = np.zeros(T)
FRp = np.zeros(T)
alfapt = np.zeros(T)
eyfunt = np.zeros(T)
CRy = np.zeros(T)
FRy = np.zeros(T)
alfayt = np.zeros(T)
anspirits = np.zeros(T)
epsilont = np.zeros(T)
etat = np.zeros(T)
p = np.zeros(T) 
y = np.zeros(T) 
plagt = np.zeros(T) 
ylagt = np.zeros(T) 
r = np.zeros(T) 
epf = np.zeros(T) 
epc = np.zeros(T) 
ep = np.zeros(T) 
ey = np.zeros(T) 
CRp = np.zeros(T) 
FRp = np.zeros(T) 
alfapt = np.zeros(T) 
eyfunt = np.zeros(T) 
CRy = np.zeros(T) 
FRy = np.zeros(T) 
alfayt = np.zeros(T) 
anspirits = np.zeros(T) 
epsilont = np.zeros(T) 
etat = np.zeros(T) 
ut = np.zeros(T)

#################################################
#heuristic model
#################################################
alfap=0.5
alfay=0.5
for t in range (1,T):
    epsilont[t] = roOut*epsilont[t-1] + sigma1*normal() #shocks in output equation (demand shock)
    etat[t]= roInf*etat[t-1] + sigma2*normal() #shocks in inflation equation (supply shock)
    ut[t] = roTayl*ut[t-1] + sigma3*normal() #shocks in Taylor rule (interest rate shock)
    epsilon = epsilont[t]
    eta = etat[t]
    u = ut[t]
    shocks = np.array([eta, a2*u+epsilon])
    epcs=p[t-1]
    if epRacional==1:
        epcs=InflacaoDesejada
    eps=alfap*epcs+(1-alfap)*epfs
    if epExtrapolacao==1:
        eps=p[t-1]
    eychar=y[t-1]
    eyfun=0+    normal()/2
    eyfunt[t]=eyfun
    eys=alfay*eychar+(1-alfay)*eyfun
    forecast = np.array([eps, eys])
    plag=p[t-1]
    ylag=y[t-1]
    rlag=r[t-1]
    lag = np.array([plag, ylag])
    smooth = a2*c3
    D = forecast*B + lag*C +rlag*smooth + shocks
    X = np.squeeze(np.asarray(linalg.solve(A,np.transpose(D))))
    p[t]= X[0] 
    y[t]= X[1]
    r[t]= c1*p[t]+c2*y[t]+c3*r[t-1]+u
    if p[t]**2==1:
        r[t]= c1*(p[t])**2+c2*y[t]+c3*r[t-1]+u
    plagt[t]=p[t-1]
    ylagt[t]=y[t-1]
    CRp[t] = ro*CRp[t-1] - (1-ro)*(epcs-p[t])**2
    FRp[t] = ro*FRp[t-1] - (1-ro)*(epfs-p[t])**2
    CRy[t] = ro*CRy[t-1] - (1-ro)*(eychar-y[t])**2
    FRy[t] = ro*FRy[t-1] - (1-ro)*(eyfun-y[t])**2
    alfap = roBH*alfapt[t-1]+(1-roBH)*math.exp(gama*CRp[t])/(math.exp(gama * CRp[t]) + math.exp(gama * FRp[t]))
    alfay = roBH*alfayt[t-1]+(1-roBH)*math.exp(gama*CRy[t])/(math.exp(gama * CRy[t]) + math.exp(gama * FRy[t]))
    alfapt[t] = alfap
    alfayt[t] = alfay
    if eychar>0:
        anspirits[t]=alfay
    if eychar<0:
        anspirits[t]=1-alfay
#testes estatisticos
time=np.arange(0,T)
autocory = np.corrcoef(y,ylagt)
autocorp = np.corrcoef(p,plagt)
coroutputanimal = np.correlate(y,anspirits)
Mean=np.mean(y)
Median=np.median(y)
Max=np.amax(y)
Min=np.amin(y)
Kurt=stats.kurtosis(y)
jbTest=stats.jarque_bera(y)
#plots
fig1 = plt.figure(1)
plt.plot(time, y)
plt.ylabel('output gap')
plt.xlabel('time')
fig2 = plt.figure(2)
plt.plot(time,p)
plt.ylabel('inflation')
plt.xlabel('time')
fig3 = plt.figure(3)
plt.plot(time,r)
plt.ylabel('interest rate')
plt.xlabel('time')
fig4 = plt.figure(4)
plt.plot(time,anspirits)
plt.ylabel('animal spirits')
plt.xlabel('time')