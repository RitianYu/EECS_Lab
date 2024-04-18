import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io
import math
from boundaryBrain import MySMClass
class MySMClass1(sm.SM):
    def __init__(self,initialState='start'):
        self.startState=initialState
    def getNextValues(self, state, inp):
        v=0.3
        eps=0.2
        if state=='start':
            output='none'
            return MySMClass.getNextValues(MySMClass,state, inp)
           
          
       
    
mySM=MySMClass1()
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





