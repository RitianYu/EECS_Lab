import lib601.util as util
import lib601.dist as dist
import lib601.distPlot as distPlot
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.sonarDist as sonarDist
import lib601.move as move
import lib601.seGraphics as seGraphics
import lib601.idealReadings as idealReadings

# For testing your preprocessor
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

preProcessTestData = [SensorInput([0.8, 1.0], util.Pose(1.0, 0.5, 0.0)),
                       SensorInput([0.25, 1.2], util.Pose(2.4, 0.5, 0.0)),
                       SensorInput([0.16, 0.2], util.Pose(7.3, 0.5, 0.0))]
testIdealReadings = ( 5, 1, 1, 5, 1, 1, 1, 5, 1, 5 )
testIdealReadings100 = ( 50, 10, 10, 50, 10, 10, 10, 50, 10, 50 )


class PreProcess(sm.SM):
    
    def __init__(self, numObservations, stateWidth):
        self.startState = (None, None)
        self.numObservations = numObservations
        self.stateWidth = stateWidth

    def getNextValues(self, state, inp):
        (lastUpdatePose, lastUpdateSonar) = state
        currentPose = inp.odometry
        currentSonar = idealReadings.discreteSonar(inp.sonars[0],self.numObservations)
        # Handle the first step
        if lastUpdatePose == None:
            return ((currentPose, currentSonar), None)
        else:
            action = discreteAction(lastUpdatePose, currentPose,
                                    self.stateWidth)
            print (lastUpdateSonar, action)
            return ((currentPose, currentSonar), (lastUpdateSonar, action))

# Only works when headed to the right
def discreteAction(oldPose, newPose, stateWidth):
    return int(round(oldPose.distance(newPose) / stateWidth))


def makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations):
    
    startDistribution = dist.squareDist(0,numStates)
# redefine this
    def observationModel(ix):
        p=0.9
        halfWidth=4
        squaredist=dist.squareDist(0,numObservations-1)
        triangledist=dist.triangleDist(ideal[ix],halfWidth,0,numObservations-1)
        deltadist=dist.DeltaDist(numObservations-1)
        return dist.MixtureDist(triangledist,dist.MixtureDist(squaredist,deltadist,0.5),p)
        # ix is a discrete location of the robot
        # return a distribution over observations in that state
    def transitionModel(a):
        print a
        def trans(oldstate):
            peak=util.clip(oldstate+a,0,numStates-1)
            halfWidth=4
            return dist.triangleDist(peak,halfWidth,0,numStates-1)
        return trans
        # a is a discrete action
        # returns a conditional probability distribution on the next state
        # given the previous state    

    return ssm.StochasticSM(startDistribution, transitionModel,
                            observationModel)

pp1=PreProcess(10,1.0)
model=makeRobotNavModel(testIdealReadings,0.0,10.0,10,10)
ppEst=sm.Cascade(pp1,seGraphics.StateEstimator(model))
print ppEst.transduce(preProcessTestData)
# Main procedure
def makeLineLocalizer(numObservations, numStates, ideal, xMin, xMax, robotY):
    stateWidth=float(xMax-xMin)/numStates
    Driver=move.MoveToFixedPose(util.Pose(xMax,robotY,0.0),maxVel=0.5)
    model=makeRobotNavModel(ideal,xMin,xMax,numStates,numObservations)
    pre_est=sm.Cascade(PreProcess(numObservations,stateWidth),seGraphics.StateEstimator(model))
    return sm.Cascade(sm.Parallel(pre_est,Driver),sm.Select(1))
