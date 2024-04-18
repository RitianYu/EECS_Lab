import lib601.dist as dist
import lib601.coloredHall as coloredHall
from lib601.coloredHall import *

possibleColors=['black','white','red','green','blue']
standardHallway=['white', 'white', 'green', 'white', 'white']
def whiteEqGreenObsDist (actualColor):
    if actualColor=='green' or actualColor=='white':
        return dist.DDist({'green':0.5,'white':0.5})
    else:
        return dist.DDist({actualColor:1.0})

def whiteVsGreenObsDist(actualColor):
    if actualColor=='green':
        return dist.DDist({'white':1.0})
    elif actualColor=='white':
        return dist.DDist({'green':1.0})
    else:
        return dist.DDist({actualColor:1.0})

def noisyObs(actualColor):
    obsColor=dict()
    for i in possibleColors:
        if i==actualColor:
            obsColor[i]=0.8
        else:
            obsColor[i]=0.05

def makeObservaionModel(hallwayColors,obsNoise):
    return lambda loc:obsNoise(hallwayColors[loc])

noisyObsModel=makeObservationModel(standardHallway,nosiyOBs)
