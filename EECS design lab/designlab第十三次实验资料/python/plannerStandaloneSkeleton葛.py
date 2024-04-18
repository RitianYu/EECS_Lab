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
    
    legalInputs = ('w','n','s','e','ne','se','ws','wn')
    
    def __init__(self, theMap):
        self.maps=theMap
        self.basiccost=theMap.xStep
        self.extracost=theMap.xStep*1.41421356
        self.basicinp=('w','n','s','e')
        self.extrainp=('ne','se','ws','wn')


    def getNextValues(self, state, inp):
        originpoint=self.maps.indicesToPoint(state)
        if inp in self.basicinp:
            if inp=='w':
                nextpoint=originpoint.add(util.Point(-self.basiccost,0))
            elif inp=='e':
                nextpoint = originpoint.add(util.Point(self.basiccost, 0))
            elif inp=='n':
                nextpoint = originpoint.add(util.Point(0, self.basiccost))
            elif inp=='s':
                nextpoint = originpoint.add(util.Point(0, -self.basiccost))
            nextindices=self.maps.pointToIndices(nextpoint)
            if self.maps.robotCanOccupy(nextindices):
                return (nextindices,self.basiccost)
            else:
                return (state,self.basiccost)
        else:
            if inp == 'ne':
                nextpoint = originpoint.add(util.Point(self.basiccost, self.basiccost))
                indices1=self.maps.pointToIndices(originpoint.add(util.Point(0, self.basiccost)))
                indices2=self.maps.pointToIndices(originpoint.add(util.Point(self.basiccost, 0)))
            elif inp == 'se':
                nextpoint = originpoint.add(util.Point(self.basiccost, -self.basiccost))
                indices1 = self.maps.pointToIndices(originpoint.add(util.Point(0, -self.basiccost)))
                indices2 = self.maps.pointToIndices(originpoint.add(util.Point(self.basiccost, 0)))
            elif inp == 'wn':
                nextpoint = originpoint.add(util.Point(-self.basiccost, self.basiccost))
                indices1 = self.maps.pointToIndices(originpoint.add(util.Point(0, self.basiccost)))
                indices2 = self.maps.pointToIndices(originpoint.add(util.Point(-self.basiccost, 0)))
            elif inp == 'ws':
                nextpoint = originpoint.add(util.Point(-self.basiccost, -self.basiccost))
                indices1 = self.maps.pointToIndices(originpoint.add(util.Point(0, -self.basiccost)))
                indices2 = self.maps.pointToIndices(originpoint.add(util.Point(-self.basiccost, 0)))
            nextindices = self.maps.pointToIndices(nextpoint)
            if self.maps.robotCanOccupy(nextindices) and self.maps.robotCanOccupy(indices1) and self.maps.robotCanOccupy(indices2):
                return (nextindices, self.extracost)
            else:
                return (state, self.extracost)




class TestGridMap(gridMap.GridMap):
    def __init__(self, gridSquareSize):
        gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
                               0, gridSquareSize * 5, gridSquareSize, 100)

    def makeStartingGrid(self):
        grid = util.make2DArray(5, 5, False)
        for i in range(5):
            grid[i][0] = True
            grid[i][4] = True
        for j in range(5):
            grid[0][j] = True
            grid[4][j] = True
        grid[3][3] = True
        return grid

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
    mapped = basicGridMap.BasicGridMap(worldPath, gridSquareSize)
    def g(s):
        mapped.drawSquare(s, 'gray')
        if s==mapped.pointToIndices(goalPoint):
            return True
    def heuristic(s):
        return mapped.indicesToPoint(s).distance(goalPoint) #The Euclidean distance
        
        # n=mapped.indicesToPoint(s)
        # goal=goalPoint
        # def h_diagonal(n):
        #     return min(abs(n.x-goal.x), abs(n.y-goal.y))
        # def h_straight(n):
        #     return (abs(n.x-goal.x) + abs(n.y-goal.y))
        # return mapped.xStep*1.41421356 * h_diagonal(n) + mapped.xStep * (h_straight(n) - 2*h_diagonal(n)) #The Diagonal distance

        #goal = goalPoint
        #node = mapped.indicesToPoint(s)
        #dx = abs(node.x - goal.x)
        #dy = abs(node.y - goal.y)
        #return mapped.xStep*(dx + dy) + (mapped.xStep*1.41421356 - 2*mapped.xStep)*min(dx, dy)  #The Chebyshev distance

        
    road=ucSearch.smSearch(GridDynamics(mapped),mapped.pointToIndices(initialPose.point()),g,heuristic)
    roadlist=[]
    for item in road:
        roadlist.append(item[1])
    mapped.drawPath(roadlist)


        

def testPlanner(world):
    (worldPath, gridSquareSize, goalPoint, initialPose) = world
    planner(initialPose, goalPoint, worldPath, gridSquareSize)


testPlanner(mapTestWorld)

