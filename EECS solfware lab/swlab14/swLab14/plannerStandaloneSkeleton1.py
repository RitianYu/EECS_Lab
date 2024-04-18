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
    legalInputs = ['up','down','left','right','up_left','up_right','down_left','down_right']
    def __init__(self, theMap):
        self.step=theMap.xStep
        self.map=theMap
    def getNextValues(self, state, inp):
        if inp=='up':
            nextstate=(state[0],state[1]+1)
            cost=self.step
            if self.map.robotCanOccupy(nextstate):
                return (nextstate,cost)
            else:
                return (state,cost)
        elif inp=='down':
            nextstate=(state[0],state[1]-1)
            cost=self.step
            if self.map.robotCanOccupy(nextstate):
                return (nextstate,cost)
            else:
                return (state,cost)
        elif inp=='left':
            nextstate=(state[0]-1,state[1])
            cost=self.step
            if self.map.robotCanOccupy(nextstate):
                return (nextstate,cost)
            else:
                return (state,cost)
        elif inp=='right':
            nextstate=(state[0]+1,state[1])
            cost=self.step
            if self.map.robotCanOccupy(nextstate):
                return (nextstate,cost)
            else:
                return (state,cost)
        elif inp=='up_left':
            nextstate=(state[0]-1,state[1]+1)
            up=(state[0],state[1]+1)
            left=(state[0]-1,state[1])
            cost=self.step*math.sqrt(2)
            if self.map.robotCanOccupy(up) and self.map.robotCanOccupy(left):
                if self.map.robotCanOccupy(nextstate):
                    return (nextstate,cost)
                else:
                    return (state,cost)
            else:
                return (state,cost)
        elif inp=='up_right':
            nextstate=(state[0]+1,state[1]+1)
            up=(state[0],state[1]+1)
            right=(state[0]+1,state[1])
            cost=self.step*math.sqrt(2)
            if self.map.robotCanOccupy(up) and self.map.robotCanOccupy(right):
                if self.map.robotCanOccupy(nextstate):
                    return (nextstate,cost)
                else:
                    return (state,cost)
            else:
                return (state,cost)
        elif inp=='down_left':
            nextstate=(state[0]-1,state[1]-1)
            down=(state[0],state[1]-1)
            left=(state[0]-1,state[1])
            cost=self.step*math.sqrt(2)
            if self.map.robotCanOccupy(down) and self.map.robotCanOccupy(left):
                if self.map.robotCanOccupy(nextstate):
                    return (nextstate,cost)
                else:
                    return (state,cost)
            else:
                return (state,cost)
        elif inp=='down_right':
            nextstate=(state[0]+1,state[1]-1)
            down=(state[0],state[1]-1)
            right=(state[0]+1,state[1])
            cost=self.step*math.sqrt(2)
            if self.map.robotCanOccupy(down) and self.map.robotCanOccupy(right):
                if self.map.robotCanOccupy(nextstate):
                    return (nextstate,cost)
                else:
                    return (state,cost)
            else:
                return (state,cost)
        else:
            return ('illegal_action','illegal_action')
    
    
#class TestGridMap(gridMap.GridMap):
#   def __init__(self, gridSquareSize):
#        gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
#                               0, gridSquareSize * 5, gridSquareSize, 100)
#
#    def makeStartingGrid(self):
#        grid = util.make2DArray(5, 5, False)
#        for i in range(5):
#            grid[i][0] = True
#            grid[i][4] = True
#        for j in range(5):
#            grid[0][j] = True
#            grid[4][j] = True
#        grid[3][3] = True
#        return grid

#    def robotCanOccupy(self, (xIndex, yIndex)):
#        return not self.grid[xIndex][yIndex]

class TestGridMap(gridMap.GridMap):
    def __init__(self, gridSquareSize):
        (self.xN, self.yN) = (5, 5)
        self.xStep = gridSquareSize
        self.yStep = gridSquareSize
        self.xMin = self.yMin = 0.0
        self.xMax = self.yMax = gridSquareSize * 5
        self.grid = util.make2DArray(5, 5, False)
        for i in range(5):
            self.grid[i][0] = True
            self.grid[i][4] = True
        for j in range(5):
            self.grid[0][j] = True
            self.grid[4][j] = True
            self.grid[3][3] = True
    def robotCanOccupy(self, (xIndex, yIndex)):
        return not self.grid[xIndex][yIndex]
    
def testGridDynamics():
    gm = TestGridMap(0.15)
    print 'For TestGridMap(0.15):'
    r = GridDynamics(gm)
    print 'legalInputs', util.prettyString(r.legalInputs)
    ans1 = [r.getNextValues((1,1), a) for a in r.legalInputs]
    print 'starting from (1,1)', util.prettyString(ans1)
    ans2 = [r.getNextValues((2,3), a) for a in r.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans2)
    ans3 = [r.getNextValues((3, 2), a) for a in r.legalInputs]
    print 'starting from (3,2)', util.prettyString(ans3)
    gm2 = TestGridMap(0.4)
    print 'For TestGridMap(0.4):'
    r2 = GridDynamics(gm2)
    ans4 = [r2.getNextValues((2,3), a) for a in r2.legalInputs]
    print 'starting from (2,3)', util.prettyString(ans4)

def planner(initialPose, goalPoint, worldPath, gridSquareSize):
    gridmap=basicGridMap.BasicGridMap(worldPath, gridSquareSize)
    gridDynamics=GridDynamics(gridmap)
    init=gridmap.pointToIndices(initialPose.point())
    goal=gridmap.pointToIndices(goalPoint)
    path=[]
    def g(s):
        gridmap.drawSquare(s,'gray')
        return s==goal
    def heuristic(s):
        return min(abs(s[0]-goal[0]),abs(s[1]-goal[1]))*(gridmap.xStep*math.sqrt(2))\
                   +(max(abs(s[0]-goal[0]),abs(s[1]-goal[1]))-min(abs(s[0]-goal[0]),abs(s[1]-goal[1])))*gridmap.xStep
    searchlist=ucSearch.smSearch(gridDynamics,init,g,heuristic)
    for i in searchlist:
        path.append(i[1])
    gridmap.drawPath(path)
    return searchlist

def testPlanner(world):
    (worldPath, gridSquareSize, goalPoint, initialPose) = world
    planner(initialPose, goalPoint, worldPath, gridSquareSize)

testPlanner(mapTestWorld)
                        


