import lib601.sf as sf
import lib601.optimize as optimize
import operator
import lib601.poly as poly

def delayPlusPropModel(k1, k2):
    T = 0.1
    V = 0.1
    
    # Controller:  your code here
    def controller(k1,k2):
        sf1=sf.Gain(k1)
        sf2=sf.Gain(k2)
        return sf.FeedforwardAdd(sf1,sf2)
    # The plant is like the one for the proportional controller.  Use
    # your definition from last week.
    def plant1(T):
       sf1=sf.Cascade(sf.R(),sf.Gain(T))
       sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
       return sf.Cascade(sf1,sf2)

    def plant2(T, V):
       sf1=sf.Cascade(sf.R(),sf.Gain(V*T))
       sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
       return sf.Cascade(sf1,sf2)

    # Combine the three parts
    sf1=sf.Cascade(controller(k1,k2),plant1(T))
    sf2=sf.Cascade(sf1,plant2(T,V))
    sys = sf.FeedbackSubtract(sf1,sf2)
    return sys

# You might want to define, and then use this function to find a good
# value for k2.

# Given k1, return the value of k2 for which the system converges most
# quickly, within the range k2Min, k2Max.  Should call optimize.optOverLine.

def anglePlusPropModel(k3, k4):
    T = 0.1
    V = 0.1
    def plant1(T):
        sf1=sf.Cascade(sf.R(),sf.Gain(T))
        sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
        return sf.Cascade(sf1,sf2)
    def plant2(T, V):
       sf1=sf.Cascade(sf.R(),sf.Gain(V*T))
       sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
       return sf.Cascade(sf1,sf2)
    sf1=sf.Gain(k3)
    sf2=sf.FeedbackSubtract(plant1(T),sf.Gain(k4))
    sf3=sf.Cascade(sf1,sf2)
    sf4=sf.Cascade(sf3,plant2(T,V))
    sys=sf.FeedbackSubtract(sf4,sf.Gain(1))
    return sys


# Given k3, return the value of k4 for which the system converges most
# quickly, within the range k4Min, k4Max.  Should call optimize.optOverLine.

def bestk4(k3, k4Min, k4Max, numSteps):
     def y(k4):
        sf1=sf.SystemFunction(poly.Polynomial([0.001*k3,0,0]),poly.Polynomial([0.001*k3-0.1*k4+1,0.1*k4-2,1]))
        return sf1.dominantPole()
     print optimize.optOverLine(y,k4Min,k4Max,numSteps)
bestk4(1, -2, 2, 10000)

def bestk2(k1, k2Min, k2Max, numSteps):
    def y(k2):
        sf1=sf.SystemFunction(poly.Polynomial([0.001*k2,0.001*k1,0,0]),poly.Polynomial([0.001*k2,(1+0.001*k1),-2,1]))
        return sf1.dominantPole()
    print optimize.optOverLine(y,k2Min,k2Max,numSteps)
#bestk2(10, -1000, 1000, 10000)
