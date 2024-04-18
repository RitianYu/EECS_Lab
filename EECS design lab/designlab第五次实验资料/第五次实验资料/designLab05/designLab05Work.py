import lib601.sig as sig
import lib601.ts as ts
import lib601.poly as poly
import lib601.sf as sf

def controller(k):
   return sf.Gain(k)

def plant1(T):
   sf1=sf.Cascade(sf.R(),sf.Gain(T))
   sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
   return sf.Cascade(sf1,sf2)

def plant2(T, V):
   sf1=sf.Cascade(sf.R(),sf.Gain(V*T))
   sf2=sf.FeedbackAdd(sf.Gain(1),sf.R())
   return sf.Cascade(sf1,sf2)

def wallFollowerModel(k, T, V):
   sf1=sf.Cascade(controller(k),plant1(T))
   sf2=sf.Cascade(sf1,plant2(T,V))
   return sf.FeedbackSubtract(sf2,sf.Gain(1))

print wallFollowerModel(1,0.1,0.1).dominantPole()

print type (poly.Polynomial([1,2,3]))
print poly.Polynomial([1,2,3]).coeff(1)
