from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math as math
import scipy.io as sio
import os
from scipy import linalg
from scipy import stats
from scipy.optimize import minimize
import time
import multiprocessing as mp


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def VectorParallel(begin, end, step, N):
    templistc1 = []
    templistc2 = []
    ar = int(abs(np.log10(step)))
    for i in frange(begin, end, step):
        for j in frange(begin, end, step):
            templistc1 = np.append(templistc1, i)
            templistc2 = np.append(templistc2, j)
    listc1 = []
    listc2 = []
    for i in range(np.size(templistc1)):
        for z in range(N):
            listc1 = np.append(listc1, round(templistc1[i], ar))
            listc2 = np.append(listc2, round(templistc2[i], ar))
    return listc1, listc2


def ExistsInVector(V, x):
    out = False
    for i in range(0, len(V)):
        if V[i] == x:
            out = True
            break
    return out


def GetNeighbours(matriz, vic):
    OutGrid = matriz[vic, :]
    nearest = []
    for i in range(0, np.size(matriz, 0)):
        if OutGrid[i] != 0 and i != vic:
            nearest = np.append(nearest, i)
    return nearest


def MakeAnHistogram(Vector, HistTitle, nBins):
    # histogram
    plt.hist(Vector, nBins)
    plt.title(HistTitle)
    plt.show()


def MakeAStem(X, Y):
    markerline, stemlines, baseline = plt.stem(X, Y, ' ')


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def StarNetwork(N):
    rede = np.zeros((N, N))
    rede[0, :] = 1
    rede[:, 0] = 1
    rede = rede + np.identity(N)
    rede[0, 0] = 1
    return rede


def PerfectNetwork(N):
    rede = np.ones((N, N))
    return rede


def SelfNetwork(N):
    rede = np.identity(N)
    return rede


def CircularNetwork(N, k):
    Neighbours = np.zeros((N, 2 * k + 1))
    Neighbours[:, 0] = np.transpose((np.linspace(0, N - 1, N)))
    for i in range(0, N):
        for z in range(0, k):
            Neighbours[i, 1 + z * 2] = i - z - 1
            Neighbours[i, z * 2 + 2] = i + z + 1
    for i in range(0, N):
        for z in range(0, 2 * k + 1):
            if Neighbours[i, z] < 0:
                Neighbours[i, z] = N + Neighbours[i, z]
            elif Neighbours[i, z] >= N:
                Neighbours[i, z] = Neighbours[i, z] - N
    rede = np.zeros((N, N))
    for i in range(0, N):
        Indexes = Neighbours[i, :]
        for j in range(0, len(Indexes)):
            index = int(Indexes[j])
            rede[i, index] = 1
    return rede


def RandomNetwork(N, k):
    rede = np.identity(N)
    for i in range(0, N):
        Indexes = np.random.permutation(N)[0:k]
        flag = False
        while flag == False:
            if ExistsInVector(Indexes, i):
                flag = False
            else:
                flag = True
                break
            Indexes = np.random.permutation(N)[0:k]
        for j in range(0, len(Indexes)):
            index = int(Indexes[j])
            rede[i, index] = 1
    return rede


def LineNetwork(N):
    Neighbours = np.zeros((N, 2 * 1 + 1))
    Neighbours[:, 0] = np.transpose((np.linspace(0, N - 1, N)))
    for i in range(0, N):
        Neighbours[i, 1] = i - 1
        Neighbours[i, 2] = i + 1
    rede = np.zeros((N, N))
    for i in range(0, N):
        Indexes = Neighbours[i, :]
        for j in range(0, len(Indexes)):
            if 0 <= Indexes[j] < N:
                index = int(Indexes[j])
                rede[i, index] = 1
    return rede
