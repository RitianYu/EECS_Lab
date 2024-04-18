import math
import lib601.sm as sm
from soar.io import io
import lib601.gfx as gfx
import lib601.util as util
import lib601.sonarDist as sonarDist

######################################################################
#
#            Brain SM
#
######################################################################

desiredRight = 0.4
forwardVelocity = 0.1
k1=300
k2=-272.7

# No additional delay
class Sensor(sm.SM):
    def getNextValues(self, state, inp):
        v = sonarDist.getDistanceRight(inp.sonars)
        print 'Dist from robot center to wall on right', v
        return (state, v)

# inp is the distance to the right
class WallFollower(sm.SM):
    def __init__(self,initial):
        self.startState=initial
    def getNextValues(self, state, inp):
        if state=='start':
            return (inp,io.Action(fvel=0,rvel=0))
        else:
            rv=(desiredRight-inp)*k1+(desiredRight-state)*k2
            return(inp,io.Action(fvel=forwardVelocity,rvel=rv))

################
# Your code here
################

sensorMachine = Sensor()
sensorMachine.name = 'sensor'
mySM = sm.Cascade(sensorMachine, WallFollower('start'))

######################################################################
#
#            Running the robot
#
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)
    robot.gfx.addStaticPlotSMProbe(y=('rightDistance', 'sensor',
                                      'output', lambda x:x))
    robot.behavior = mySM
    robot.behavior.start(traceTasks = robot.gfx.tasks())

def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())

def brainStop():
    pass
