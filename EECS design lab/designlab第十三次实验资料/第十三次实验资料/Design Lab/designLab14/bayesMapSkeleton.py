import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap


# Define the stochastic state-machine model for a given cell here.

# Observation model:  P(obs | state)
def oGivenS(s):
    if s=='occupied':
        return dist.DDist({'hit':0.9,'free':0.1})
    elif s=='not_occupied':
        return dist.DDist({'hit':0.1,'free':0.9})
    else:
        return None
# Transition model: P(newState | s | a)
def uGivenAS(a):
    def nsGivenS(s):
        if s=='occupied':
            return dist.DDist({'occupied':1.0,'not_occupied':0.0})
        elif s=='not_occupied':
            return dist.DDist({'occupied':0.0,'not_occupied':1.0})
        else:
            return None                      
    return nsGivenS
    
startDistribution=dist.DDist({'occupied':0.5,'not_occupied':0.5})         
cellSSM = ssm.StochasticSM(startDistribution,uGivenAS,oGivenS)  # Your code here

class BayesGridMap(dynamicGridMap.DynamicGridMap):
    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex,yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        elif self.occupied((xIndex, yIndex)):
            return 'black'
        else:
            return 'red'     
    def occProb(self, (xIndex, yIndex)):
        SM=self.grid[xIndex][yIndex]
        occprob=SM.state.d['occupied']
        return occprob
    def makeStartingGrid(self):
        def f(x,y):
            return seFast.StateEstimator(cellSSM)
        startGrid=util.make2DArrayFill(self.xN,self.yN,f)
        for i in range(self.xN):
            for k in range(self.yN):
                startGrid[i][k].start()
        return startGrid
    def setCell(self, (xIndex, yIndex)):
        SM=self.grid[xIndex][yIndex]
        SM.step(('hit',None))
        self.drawSquare((xIndex,yIndex))      
    def clearCell(self, (xIndex, yIndex)):
        SM=self.grid[xIndex][yIndex]
        SM.step(('free',None))
        self.drawSquare((xIndex,yIndex))          
    def occupied(self, (xIndex, yIndex)):
        threshold=0.9
        if self.occProb((xIndex,yIndex))>=threshold:
            return True
        else:
            return False
  
mostlyHits = [('hit', None), ('hit', None), ('hit', None), ('free', None)]
mostlyFree = [('free', None), ('free', None), ('free', None), ('hit', None)]

def testCellDynamics(cellSSM, input):
    se = seFast.StateEstimator(cellSSM)
    return se.transduce(input)



