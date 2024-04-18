import math
import lib601.sonarDist as sonarDist
import lib601.sm as sm
import lib601.util as util
import lib601.gridMap as gridMap
import lib601.dynamicGridMap as dynamicGridMap
import lib601.dynamicCountingGridMap as dynamicCountingGridMap
import bayesMapSkeleton as bayesMap
reload(bayesMap)

class MapMaker(sm.SM):
    def __init__(self, xMin=False, xMax=False, yMin=False, yMax=False, gridSquareSize=False):
         #self.startState = dynamicGridMap.DynamicGridMap(xMin,xMax,yMin,yMax,gridSquareSize) # in step3 and step7 uncomment this,
         self.startState = bayesMap.BayesGridMap(xMin,xMax,yMin,yMax,gridSquareSize) #in step15 and robot race, uncomment this line
    def getNextValues(self, state, inp):
        for i in range(8):
            start=state.pointToIndices(sonarDist.sonarHit(0,sonarDist.sonarPoses[i],inp.odometry))
            #the location of the sonars in the robot(It has been converted into the indices of the grid)
            if inp.sonars[i]<sonarDist.sonarMax:
                item=state.pointToIndices(sonarDist.sonarHit(inp.sonars[i],sonarDist.sonarPoses[i],inp.odometry))
                # the location of the item detected by sonars(It has been converted into the indices of the grid)
                state.setCell(item)
                # mark this grid which is occupied
            else:
                item=state.pointToIndices(sonarDist.sonarHit(sonarDist.sonarMax,sonarDist.sonarPoses[i],inp.odometry))
                # when the sonar reading is greater than the maximum good value\
                # we make the cells along the first part of the ray clear.
            clearlist=util.lineIndices(start,item)
            for i in range(len(clearlist)-1):
                state.clearCell(clearlist[i])
            # We think of these cells as the set of grid locations that could reasonably be marked as being clear,
            # based on a sonar measurement.
        return (state,state)
            
# For testing your map maker
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

testData = [SensorInput([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                        util.Pose(1.0, 2.0, 0.0)),
            SensorInput([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                        util.Pose(4.0, 2.0, -math.pi))]

testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(1.0, 2.0, 0.0)),
                 SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(4.0, 2.0, -math.pi))]

def testMapMaker(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerClear(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    for i in range(50):
        for j in range(50):
            mapper.startState.setCell((i, j))
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerN(n, data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data*n)
    print data*n
    mapper.startState.drawWorld()

testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(1.0, 2.0, 0.0)),
                 SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(4.0, 2.0, -math.pi))]

#testMapMaker(testData) #step3
#testMapMakerClear(testClearData) #step7
#testMapMakerN(1, testData)  #step15
#testMapMakerN(2, testData)  #


