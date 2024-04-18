import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io
import math
class MySMClass(sm.SM):
    def __init__(self,initialState='start'):
        self.startState=initialState
    def getNextValues(self, state, inp):
        v=0.3
        eps=0.05
        f=min(inp.sonars[3:5])
        r=inp.sonars[7]
        l=inp.sonars[0]
        if state=='start':
            if r>0.6:
                state='go_forward'
                return(state,io.Action(fvel=0,rvel=0))
            else:
                state='follow_wall'
                return(state,io.Action(fvel=v,rvel=0))
        if state=='go_forward' :
            if inp.sonars[3]>=0.3:
                return(state,io.Action(fvel=v,rvel=0))
            else:
                state=='turnleft'
                return (state,io.Action(fvel=0,rvel=v))          
        if state=='follow_wall':
            if inp.sonars[3]>=0.3:
                if r<0.4:
                    return(state,io.Action(fvel=v,rvel=0))
                else:
                    state='turnright'
                    return(state,io.Action(fvel=0,rvel=v))
            else:
                state='turnleft'
                return (state,io.Action(fvel=0,rvel=v))
        if state=='turnleft':
            if abs(inp.sonars[3]-0.3)>eps:
                state='adjust'
                return (state,io.Action(fvel=0.01,rvel=v/2))
            else:
                return (state,io.Action(fvel=0,rvel=v))            
        if state=='adjust':
            if abs(r-0.18)<eps:
                state='follow_wall'
                return (state, io.Action(fvel=v,rvel=0))
            else:
                state='adjust'
                return (state,io.Action(fvel=0.005,rvel=v/2))
       
    
mySM=MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass




