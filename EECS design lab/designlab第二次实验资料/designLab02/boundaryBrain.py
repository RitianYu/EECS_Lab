import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io
import math
class MySMClass(sm.SM):
    startState = ['start','start','start','start']
    def __init__(self,startState):
        self.state=startState
    def getNextValues(self, state, inp):
        v=0.3
        epsilon=0.01
        thetaDesire=math.pi/2-epsilon
        if state==['start','start','start','start']:
            if inp.sonars[7]>0.5:
                state=['go_forward',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=0,rvel=0))
            else:
                state=['follow_wall',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=v,rvel=0))
        if state[0]=='go_forward' and inp.sonars[3]>=0.3:
            state=[state[0],inp.odometry.theta,inp.odometry.y,inp.odometry.x]
            return(state,io.Action(fvel=v,rvel=0)) 
        if state[0]=='follow_wall' and inp.sonars[3]>=0.3:
            if inp.sonars[7]<0.5:
                state=[state[0],inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=v,rvel=0))
            if inp.sonars[7]<5:
                if abs(state[2]-inp.odometry.y)<0.5 and abs(state[3]-inp.odometry.x)<0.5:
                    state=[state[0],inp.odometry.theta,state[2],state[3]]
                    return(state,io.Action(fvel=v,rvel=0))
                else:
                    state=['turnright',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                    return(state,io.Action(fvel=0,rvel=-v))
            else:
                if inp.sonars[3]>=1.2:
                    if abs(state[2]-inp.odometry.y)<0.5 and abs(state[3]-inp.odometry.x)<0.5:
                        state=[state[0],inp.odometry.theta,state[2],state[3]]
                        return(state,io.Action(fvel=v,rvel=0))
                    else:
                        state=['turnright',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                        return(state,io.Action(fvel=0,rvel=-v))
                else:
                    state[0]='rotate'
                    return(state,io.Action(fvel=v*0.46,rvel=-v))    
        if state[0]=='go_forward' and inp.sonars[3]<0.3:
            state=['turnleft',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
            return(state,io.Action(fvel=0,rvel=v))
        if state[0]=='follow_wall' and inp.sonars[3]<0.3:
            state=['turnleft',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
            return(state,io.Action(fvel=0,rvel=v))
        if state[0]=='turnleft':
            if abs(inp.odometry.theta-state[1])<thetaDesire:
                state=['turnleft',state[1],inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=0,rvel=v))
            else:
                state=['follow_wall',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=v,rvel=0))
        if state[0]=='turnright':
            if abs(state[1]-inp.odometry.theta)<thetaDesire:
                state=['turnright',state[1],inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=0,rvel=-v))
            else:
                state=['follow_wall',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=v,rvel=0))
        if state[0]=='rotate':
            if abs(state[1]-inp.odometry.theta)<math.pi:
                return(state,io.Action(fvel=v*0.46,rvel=-v))
            else:
                state=['follow_wall',inp.odometry.theta,inp.odometry.y,inp.odometry.x]
                return(state,io.Action(fvel=v,rvel=0))
            
        return(state,io.Action(fvel=0,rvel=0))

startState = ['go_forward','start','start']
mySM=MySMClass(startState)
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
    print inp.sonars[3],inp.sonars[7],inp.odometry.theta
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass


