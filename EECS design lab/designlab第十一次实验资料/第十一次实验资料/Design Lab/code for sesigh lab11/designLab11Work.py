import lib601.dist as dist
import lib601.coloredHall as coloredHall
from lib601.coloredHall import *
import lib601.util as util
import math

standardHallway = ['white', 'white', 'green', 'white', 'white']
alternating = ['white', 'green'] * 6
sterile = ['white'] * 16
testHallway = ['chocolate', 'white', 'green', 'white', 'white',
               'green', 'green', 'white',  
               'green', 'white', 'green', 'chocolate']

maxAction = 5
actions = [str(x) for x in range(maxAction) + [-x for x in range(1, maxAction)]]

sonarMax=1.5
numObservations=10
sonarPose0=util.Pose(0.08,0.134,1.570796)

def incrDictEntry(d, k, v):
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v
 
def makePerfect(hallway = standardHallway):
    return makeSim(hallway, actions, perfectObsNoiseModel,
                   standardDynamics, perfectTransNoiseModel,'perfect')

def makeNoisy(hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'noisy')

def makeNoisyKnownInitLoc(initLoc, hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'known init',
                    initialDist = dist.DDist({initLoc: 1}))

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

noisyObsModl=makeObservationModel(standardHallway,noisyObs)

def ringDynamics(loc,act,hallwayLength):
    if loc+act>hallwayLength-1:
        return loc+act-hallwayLength
    elif loc+act<0:
        return hallwayLength+(loc+act)
    else:
        return loc+act

def leftSlipTrans(nominalLoc, hallwayLength):
    if nominalLoc>0:
        return dist.DDist({nominalLoc:0.9,nominalLoc-1:0.1})
    else:
        return dist.DDist({nominalLoc:1})

def noisyTrans(nominalLoc,hallwayLength):
    if nominalLoc>0 and nominalLoc<hallwayLength-1:
        return dist.DDist({nominalLoc:0.8,nominalLoc-1:0.1,nominalLoc+1:0.1})
    elif nominalLoc==0:
        return dist.DDist({nominalLoc:0.9, nominalLoc+1:0.1})
    elif nominalLoc==hallwayLength:
        return dist.DDist({nominalLoc:0.9, nominalLoc-1:0.1})
    else:
        return 'wrong nominalLoc'

def makeTransitionModel(dynamics, noiseDist, hallwayLength):
    return lambda act: lambda loc: noiseDist(dynamics(loc,act,hallwayLength),hallwayLength)
    
noisyTransModel=makeTransitionModel(standardDynamics,noisyTrans,standardHallway)

def sonarHit(distance,sonarPose,robotPose):
    relative_x=sonarPose.x+distance*math.cos(sonarPose.theta)
    relative_y=sonarPose.y+distance*math.sin(sonarPose.theta)
    target_point=util.Point(relative_x,relative_y)
    return robotPose.transformPoint(target_point)

def discreteSonar(sonarReading):
    binWidth=sonarMax/numObservations
    if sonarReading>=sonarMax:
        return numObservations-1
    else:
        return int(sonarReading/binWidth)

def idealReadings(wallSegs,robotPoses):
    bin_length=sonarMax/numObservations
    sonarline=[]
    idealreading=[]
    for i in range(len(robotPoses)):
        d=[]
        p1=sonarHit(0,sonarPose0,robotPoses[i])
        p2=sonarHit(sonarMax,sonarPose0,robotPoses[i])
        sonarline.append(util.LineSeg(p1,p2))
        for k in range(len(wallSegs)):
            inter_point=sonarline[i].intersection(wallSegs[k])
            print inter_point
            if inter_point:
                d.append(p1.distance(inter_point))
            else:
                d.append(sonarMax)
        idealreading.append(discreteSonar(min(d)))
    return idealreading
        
def wall((x1, y1), (x2, y2)):
    return util.LineSeg(util.Point(x1,y1), util.Point(x2,y2))
wallSegs = [wall((0, 2), (8, 2)),
wall((1, 1.25),(1.5, 1.25)),
wall((2, 1.75),(2.8, 1.75))]
robotPoses = [util.Pose(0.5, 0.5, 0), util.Pose(1.25, 0.5,0),util.Pose(1.75, 1.0, 0), util.Pose(2.5, 1.0, 0)]        
print idealReadings(wallSegs,robotPoses)        
    
    
