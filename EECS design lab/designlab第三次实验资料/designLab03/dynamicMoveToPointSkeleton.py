# -*- coding: cp936 -*-
import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
import lib601.io as io
# Use this line for testing in soar
from soar.io import io

p0=util.Point(0,1)
p1=util.Point(-0.5,0.5)
print p0.angleTo(p1)
class DynamicMoveToPoint(sm.SM):
    def getNextValues(self, state, inp):
        # Replace this definition
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'
        p0=util.Point(inp[1].odometry.x,inp[1].odometry.y) 
        p1=inp[0]
        angleEps=0.01
        distEps=0.01
        thetaDesire=util.fixAngle02Pi(p0.angleTo(p1))
        if not util.nearAngle(inp[1].odometry.theta,thetaDesire,angleEps):
            if abs(inp[1].odometry.theta<=thetaDesire) and abs(inp[1].odometry.theta-thetaDesire)<=math.pi:
                state='turnleft'
                return (state, io.Action(fvel=0,rvel=0.15))
            else:
                state='turnright'
                return (state,io.Action(fvel=0,rvel=-0.15))
        else:
            state='go_straight'
            if not p1.isNear(inp[1].odometry.point(),distEps):
                return(state,io.Action(fvel=0.2,rvel=0))
            else:
                return(state,io.Action(fvel=0,rvel=0))

    
    
