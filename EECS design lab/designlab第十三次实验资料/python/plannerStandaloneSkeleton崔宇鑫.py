import math
import lib601.ucSearch as ucSearch
import lib601.util as util
import lib601.basicGridMap as basicGridMap
import lib601.gridMap as gridMap
import lib601.sm as sm



######################################################################
###         Picking worlds
######################################################################

mapTestWorld = ['mapTestWorld.py', 0.2, util.Point(2.0, 5.5),
                util.Pose(2.0, 0.5, 0.0)]
bigPlanWorld = ['bigPlanWorld.py', 0.25, util.Point(3.0, 1.0),
                util.Pose(1.0, 1.0, 0.0)]


class GridDynamics(sm.SM): 
    legalInputs =  [(dx, dy) for dx in (-1, 0, 1)
                             for dy in (-1, 0, 1) if dx != 0 or dy != 0]
    def __init__(self, theMap):
        self.theMap = theMap
    def getNextValues(self, state, inp):
        ix, iy = state
        dx, dy = inp
        New_X, New_Y = ix+dx, iy+dy
        cost =  math.sqrt((dx * self.theMap.xStep) ** 2
                          + (dy * self.theMap.yStep) ** 2)
        if self.theMap.robotCanOccupy((New_X, New_Y)):
            if dx!=0 and dy!=0:
                if self.theMap.robotCanOccupy((ix, New_Y)) and self.theMap.robotCanOccupy((New_X, iy)):
                    return ((New_X, New_Y), cost)
                else:
                    return ((ix, iy), cost)
            else:
                return ((New_X, New_Y), cost)
        else:
            return ((ix, iy), cost)



##class TestGridMap(gridMap.GridMap):
##    def __init__(self, gridSquareSize):
##        gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
##                               0, gridSquareSize * 5, gridSquareSize, 100)
##
##    def makeStartingGrid(self):
##        grid = util.make2DArray(5, 5, False)
##        for i in range(5):
##            grid[i][0] = True
##            grid[i][4] = True
##        for j in range(5):
##            grid[0][j] = True
##            grid[4][j] = True
##        grid[3][3] = True
##        return grid
##
##    def robotCanOccupy(self, (xIndex, yIndex)):
##        return not self.grid[xIndex][yIndex]
##
##def testGridDynamics():
##    gm = TestGridMap(0.15)
##    print 'For TestGridMap(0.15):'
##    r = GridDynamics(gm)
##    print 'legalInputs', util.prettyString(r.legalInputs)
##    ans1 = [r.getNextValues((1,1), a) for a in r.legalInputs]
##    print 'starting from (1,1)', util.prettyString(ans1)
##    ans2 = [r.getNextValues((2,3), a) for a in r.legalInputs]
##    print 'starting from (2,3)', util.prettyString(ans2)
##    ans3 = [r.getNextValues((3, 2), a) for a in r.legalInputs]
##    print 'starting from (3,2)', util.prettyString(ans3)
##    gm2 = TestGridMap(0.4)
##    print 'For TestGridMap(0.4):'
##    r2 = GridDynamics(gm2)
##    ans4 = [r2.getNextValues((2,3), a) for a in r2.legalInputs]
##    print 'starting from (2,3)', util.prettyString(ans4)
##
##print testGridDynamics()

def planner(initialPose, goalPoint, worldPath, gridSquareSize):
    gm = basicGridMap.BasicGridMap(worldPath, gridSquareSize)
    initialState = gm.pointToIndices(initialPose.point())
    goalStates = gm.pointToIndices(goalPoint)

    def g(s):
        gm.drawSquare(s, 'gray')
        return s == goalStates
    def heuristic(s):
        return math.sqrt(((goalStates[0]-s[0])* gm.xStep)**2+((goalStates[1]-s[1])*gm.yStep)**2)

    path = ucSearch.smSearch(GridDynamics(gm), initialState,
                             goalTest = lambda state: g(state),
                             heuristic = lambda state: heuristic(state))

##    path = ucSearch.smSearch(GridDynamics(gm), initialState,
##                             goalTest = lambda state: g(state))
    best_path = []
    best_path = [path[i][1] for i in range(len(path))]
    gm.drawPath(best_path)
    return path
    

def testPlanner(world):
    (worldPath, gridSquareSize, goalPoint, initialPose) = world
    planner(initialPose, goalPoint, worldPath, gridSquareSize)

testPlanner(mapTestWorld)
