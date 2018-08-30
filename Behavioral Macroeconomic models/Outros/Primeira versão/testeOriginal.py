from __future__ import division
import numpy as np
import matplotlib.pyplot as plt	
import math as math
import scipy as sc
from scipy import linalg
#parametros do modelo
gamma=10 #parametro de mudanca gama no modelo de Brock Hommes
TargetInf=0 #inflacao desejada do banco central
epRational=0 #previsao racional da inflacao (=1)
epExtrapolation=0 #previsao extrapolativa da inflacao (=1)
InflacaoDesejada=0
a1=0.5 #coeficiente do output esperado na eq do output gap
a2=-0.2 #elasticidade da taxa de juro na eq do output gap
b1=0.5 #coeficiente da inflacao esperada na eq da inflacao
b2=0.05 #coeficiente de output na eq da inflacao
c1=1.5 #coeficiente da inflacao na eq de Taylor
c2=0.5 #coeficiente do outputgap na eq de Taylor
c3=0.5 #parametro de suavidade da taxa de juro eq de Taylor
A=np.matrix([[1, -b2], [-a2*c1, 1-a2*c2]])
B= np.matrix([[b1,0],[-a2,a1]])
C=np.matrix([[1-b1, 0],[0, 1-a1]])
T=100
sigma1=0.5 #desvio padrao choque da eq do output gap
sigma2=0.5 #desvio padrao choque da eq da inflacao
sigma3=0.5 #desvio padrao choque da eq de Taylor
ro=0 #ro na media dos erros quadrados
roOut=0.0 #ro nos choques na eq do output gap
roInf=0.0 #ro nos choques na eq da inflacao
roTayl=0.0 #ro nos choques na equacao de Taylor
roBH=0.0 #ro do modelo de Brock Homes
epfs=InflacaoDesejada #forecast inflation targeters
p=np.zeros((T,1))
y=np.zeros((T,1))
plagt=np.zeros((T,1))
ylagt=np.zeros((T,1))
r=np.zeros((T,1))
epf=np.zeros((T,1))
epc=np.zeros((T,1))
ep=np.zeros((T,1))
ey=np.zeros((T,1))
CRp=np.zeros((T,1))
FRp=np.zeros((T,1))
alfapt=np.zeros((T,1))
eyfunt=np.zeros((T,1))
CRy=np.zeros((T,1))
FRy=np.zeros((T,1))
alfayt=np.zeros((T,1))
anspirits=np.zeros((T,1))
epsilont=np.zeros((T,1))
etat=np.zeros((T,1))
ut=np.zeros((T,1))
#################################################
#heuristic model
#################################################
alfap=0.5
alfay=0.5
for t in range (1,T):
        epsilont[t]=roOut*epsilont[t-1] + sigma1*np.random.randn() #shocks in output equation (demand shock)
        etat[t]= roInf*etat[t-1] + sigma2*np.random.randn() #shocks in inflation equation (supply shock)
        ut[t]=roTayl*ut[t-1] + sigma3*np.random.randn() #shocks in Taylor rule (interest rate shock)
        epsilon=epsilont[t]
        eta=etat[t]
        u=ut[t]
        shocks=np.array([eta,a2*u+epsilon])
        epcs=p[t-1]
        if epRational==1:
            epcs=TargetInf
        eps=alfap*epcs+(1-alfap)*epfs
        if epExtrapolation==1:
            eps=p[t-1]
        eyfun=0+np.random.randn()/2
        eyfunt[t]=eyfun
        eys=alfay*eychar+(1-alfay)*eyfun
        forecast=np.array([eps,eys])
        plag=p[t-1]
        ylag=y[t-1]
        rlag=r[t-1]
        lag=np.array([plag, ylag])
        smooth=np.array([0 ,a2*c3])
        D=B.dot(forecast) + C.dot(lag) + rlag*smooth.reshape((-1,1)) + shocks
        #X=A/D
        X=linalg.solve(A,D)
        p[t]= X[0]
        y[t]= X[1]
        r[t]= c1*p[t]+c2*y[t]+c3*r[t-1]+u
        if p[t]**2==1:
            r[t]= c1*(p[t])**2+c2*y[t]+c3*r[t-1]+u
        plagt[t]=p[t-1]
        ylagt[t]=y[t-1]
        CRp[t]=ro*CRp[t-1] - (1-ro)*(epcs-p[t])**2
        FRp[t]=ro*FRp[t-1] - (1-ro)*(epfs-p[t])**2
        CRy[t]=ro*CRy[t-1] - (1-ro)*(eychar-y[t])**2
        FRy[t]=ro*FRy[t-1] - (1-ro)*(eyfun-y[t])**2
        alfap=roBH*alfapt[t-1]+(1-roBH)*math.exp(gamma*CRp[t])/(math.exp(gamma * CRp[t]) + math.exp(gamma * FRp[t]))
        alfay=roBH*alfayt[t-1]+(1-roBH)*math.exp(gamma*CRy[t])/(math.exp(gamma * CRy[t]) + math.exp(gamma * FRy[t]))
        alfapt[t]=alfap
        alfayt[t]=alfay
        if eychar>0:
            anspirits[t]=alfay
        if eychar<0:
            anspirits[t]=1-alfay
time=np.arange(0,T)
#plots
fig1 = plt.figure(1)
plt.plot(time, y)
plt.ylabel('output gap')
plt.xlabel('time')
plt.show()
fig2 = plt.figure(2)
plt.plot(time,p)
plt.ylabel('inflation')
plt.xlabel('time')
plt.show()
fig3 = plt.figure(3)
plt.plot(time,r)
plt.ylabel('interest rate')
plt.xlabel('time')
plt.show()
fig4 = plt.figure(4)
plt.plot(time,anspirits)
plt.ylabel('animal spirits')
plt.xlabel('time')
plt.show()
pass
