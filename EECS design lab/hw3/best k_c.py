# -*- coding: cp936 -*-
import lib601.sf as sf
import lib601.sig as sig
import lib601.ts as ts

import operator

import lib601.optimize as optimize
# 6.01 HomeWork 2 Skeleton File

#Constants relating to some properties of the motor
k_m = 250
k_b = 0.48
k_s = 2.5
r_m = 4.5


T=0.02

def controllerAndSensorModel(k_c):

    return sf.Gain(k_c*k_s)

    pass #your code here
    
def integrator(T):

    return sf.Cascade(sf.Cascade(sf.R(),sf.Gain(T)),sf.FeedbackAdd(sf.Gain(1),sf.R()))
    
    pass #your code here

def motorModel(T):

    return sf.FeedbackSubtract(sf.Cascade(sf.Cascade(sf.Gain(k_m/r_m),sf.R()),sf.Cascade(sf.Gain(T),sf.FeedbackAdd(sf.Gain(1),sf.R()))),sf.Gain(k_b))
    
    pass #your code here

def plantModel(T):

    return sf.Cascade(motorModel(T),integrator(T))
    
    pass #your code here

def lightTrackerModel(T,k_c):

    return sf.FeedbackSubtract(sf.Cascade(controllerAndSensorModel(k_c),plantModel(T)))
    
    pass #your code here


def plotOutput(sfModel):
    """Plot the output of the given SF, with a unit-step signal as input"""
    smModel = sfModel.differenceEquation().stateMachine()
    outSig = ts.TransducedSignal(sig.StepSignal(), smModel)
    outSig.plot()

xmin=-4
xmax=4
numXsteps = 10000

fastest_k_c = optimize.optOverLine(lambda k_c: abs(lightTrackerModel(T,k_c).dominantPole()),xmin,xmax,numXsteps)

print(fastest_k_c,'k_s =',k_s)

