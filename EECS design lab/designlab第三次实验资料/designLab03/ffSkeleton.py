import lib601.sm as sm
import lib601.util as util
import math
import lib601.io as io
#from soar.io import io
points=[util.Point(0.5, 0.5), util.Point(0.0, 1.0),
        util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]
class FollowFigure(sm.SM):
    def __init__(self,state):
        self.startState=state
    def getNextValues(self,state,inp):
        angleEps=0.01
        distEps=0.01
        if len(state)>1:
            if  state[0].isNear(inp.odometry.point(),distEps):
                state=state[1:]
                output=state[0]
                return (state,output)
            else:
                output=state[0]
                return (state,output)
        else:
            output=state[0]
            return (state,output)
            
        
