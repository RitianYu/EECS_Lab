import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
    print 'setting labPath to', labPath

from boundaryFollower import boundaryFollowerClass

eps=0.1
dDesired=0.5
class MySMClass(sm.SM):
    def __init__(self,initialValue='start'):
        self.startState=initialValue
    def getNextValues(self, state, inp):
        if self.state=='start':
            initial_alpha=inp.analogInputs[0]/10
            return (initial_alpha,io.Action(fvel=0,rvel=0))
        else:
            current_alpha=inp.analogInputs[0]/10
            delta=current_alpha-state
            if abs(delta)>eps:
                if delta>0:
                    return (state,io.Action(fvel=0,rvel=K*delta))
                if delta<0:
                    return (state,io.Action(fvel=0,rvel=-K*delta))
            else:
                if (inp.analogInputs[1]/inp.analogInputs[2])>0.5:  
                    return (state,io.Action(fvel=K*(inp.sonars[3]-dDesired,)rvel=0))
                else:
                    return (state,io.Action(fvel=0,rvel=0))
        
            
def condition(inp):
    if (inp.analogInputs[1]/inp.analogInputs[2])<0.5:
        return False
    else:
        for i in range(8):
            if inp.sonars[i]>0.5:
                return True
            else:
                return False
    
mySM =sm.Switch(condition,MySMClass,boundaryFollowerClass())
mySM.name = 'brainSM'
    

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []

def step():
    inp = io.SensorInput()
    print inp.sonars[6]

    robot.behavior.step(inp).execute()

def brainStop():
    pass

def shutdown():
    pass
