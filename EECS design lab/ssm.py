#-----------STOCHASTIC STATE MACHINE----------------
#
#	The following library implements discrete distributions,
#	stochastic state machines and state estimators.
#
#
#	Scott's Note: This project was not fully completed, as the SSM
#	only works without input, since a fully generalized JDist class
#	wasn't created. It's only a demonstration, so full testing suites
#	and correct modularization have also not been fully implemented
#
#---------------------------------------------------

import sm
import random



#-----Discrete Distribution----------
#	The following class stores discrete distributions
#	by using a dictionary which associates events and
# 	their probabilities
#------------------------------------
class DDist():
	def __init__(self, dictionary):
		self.d = dictionary

	#returns the probability of an event
	def prob(self, event):
		if event in self.d:
			p = self.d[event]
		else:
			p = 0
		return p
	
	#returns a list of all possible events
	def support(self):
		return [k for k in self.d.keys() if self.prob(k) > 0]
		
	#draws an element from the distribution
	def draw(self):
		r = random.random()
		probSum = 0.0
		for event in self.support():
			probSum += self.prob(event)
			if r < probSum:
				return event
				
		print "Error: draw() failed to find an event."
		return None
		
	def output(self):
		for k in self.support():
			print k,": ",self.d[k],"\n"
		
def testSuite_DDist():
	chance = 1.0/6.0
	die = DDist({1:chance,2:chance,3:chance,4:chance,5:chance,6:chance})
	weightedDie = DDist({1:chance/2,2:chance/2,3:chance,4:chance,5:chance*2,6:chance*2})
	print die.support()
	for i in range(10):
		print die.draw()
	for i in range(10):
		print weightedDie.draw()
		
#------JOINT DISTRIBUTION--------------
#	This class allows you to create a joint distribution
#	given a distribution and a function for calculating
#	the conditional distribution given that distribution
#--------------------------------------
class JDist(DDist):
	
	#Takes a distribution of a random variable and the
	#function which determines the conditional distribution
	def __init__(self, pA, pBgivenA):
		self.d = {}
		possibleAs = pA.support()
		for a in possibleAs:
			conditional = pBgivenA(a)
			for b in conditional.support():
				self.d[(a,b)] = pA.prob(a)*conditional.prob(b)
				
	#returns the individual distribution of just one of the
	#two random variable components			
	def marginalizeOut(self, variable):			
		newD = {}
		for event in self.d.keys():
			newEvent = removeElt(event, variable)
			incrDictEntry(newD, newEvent, self.prob(event))
 		return(DDist(newD))

	#returns the distribution of a variable, given the value
	#of the other variable
	def conditionOn(self, variable, value):
		newD = {}
		totalProb = 0.0
		
		#first construct an incomplete distribution, with only
		#the joint probabilities of valued elements
		for event in self.d.keys():
			if event[variable] == value:
				indivProb = self.d[event]
				totalProb += indivProb
				newEvent = removeElt(event, variable)
				newD[newEvent] = indivProb
		
		#divide by the total sub-probability to ensure all
		#probabilities sum to 1
		for subEvent in newD.keys():
			newD[subEvent] /= totalProb
		
		return(DDist(newD))
				
	def output(self):
		for event in self.d.keys():
			print "Event ",event," has a ",self.prob(event)," probability."
			
def removeElt(items, i):
	result = items[:i] + items[i+1:]
	if len(result)==1:
		return result[0]
	else:
		return result

def incrDictEntry(d, k, v):
	if d.has_key(k):
		d[k] += v
	else:
		d[k] = v			
			
def testSuite_JDist():
	pIll = DDist({'disease':.01, 'no disease':.99})
	def pSymptomGivenIllness(status):
		if status == 'disease':
			return(DDist({'cough':.9, 'none':.1}))
		elif status == 'no disease':
			return(DDist({'cough':.05, 'none':.95}))
	
	jIllnessSymptoms = JDist(pIll, pSymptomGivenIllness)
	
	jIllnessSymptoms.output()
	
	dSymptoms = jIllnessSymptoms.marginalizeOut(0)
	print "Symptoms include: \n", dSymptoms.d	
	
	symptomsGivenIll = jIllnessSymptoms.conditionOn(0,'no disease')
	print "Symptoms given no disease: \n", symptomsGivenIll.d
	
#===================STOCHASTIC STATE MACHINE===================

class SSM(sm.SM):
	def __init__(self, prior, transition, observation):
		self.prior = prior
		self.transition = transition
		self.observation = observation
		
	def startState(self):
		return self.prior.draw()
	
	def getNextValues(self, state, inp):
		return(self.transition(inp)(state).draw(), self.observation(state).draw())
		
def testSuite_SSM():
	
	prior = DDist({'good':0.9, 'bad':0.1})

	def observationModel(state):
		if state == 'good':
			return DDist({'perfect':0.8, 'smudged':0.1, 'black':0.1})
		else:
			return DDist({'perfect':0.1, 'smudged':0.7, 'black':0.2})
	
	def transitionModel(input):
		def transitionGivenInput(oldState):
			if oldState == 'good':
				return DDist({'good':0.7, 'bad':0.3})
			else:
				return DDist({'good':0.1, 'bad':0.9})
		return transitionGivenInput
			
	copyMachine = SSM(prior,transitionModel,observationModel)
	
	print copyMachine.transduce(['copy']*20)
	
#==========STOCHASTIC STATE ESTIMATOR==============	
	
class SSE(sm.SM): 	
	
	def __init__(self, machine):
		self.machine = machine
		self.startState = machine.prior
		self.transitionModel = machine.transition
		self.observationModel = machine.observation
		
	#Keep in mind for a Stochastic State Estimator the input
	#must be the last observed value and the state is the Bayesian
	#Machine's degree of belief, expressed as a probability distribution
	#over all known internal states belonging to the SSM	
	def getNextValues(self, state, inp):
		
		#First, calculate an updated belief of the last state, given
		#the known output
		
		
		#Calculates Pr(S|O = obs)
		belief = JDist(state, self.observationModel).conditionOn(1, inp)
		
		
		#Second, run the belief state through the transition model
		#to predict the current state of the machine
		n=0
		partialDist={}
		for possibility in belief.d.keys():							#go through all states
			partialDist[n] = self.transitionModel(0)(possibility).d	#figure out what would happen, were you in that state
			for event in partialDist[n].keys():
				partialDist[n][event] *= belief.prob(possibility)	#multiply by the chance you actually were in that state
			n+=1
		totalDist = partialDist[0]
		for event in partialDist[0].keys():		
			for count in range(1, n):
				totalDist[event] += partialDist[count][event]			#sum up the partial probabilities
				
		beliefPrime = DDist(totalDist)
		
		
		return (beliefPrime, beliefPrime)		
		
def testSuite_SSE():
	
	prior = DDist({'good':0.9, 'bad':0.1})

	def observationModel(state):
		if state == 'good':
			return DDist({'perfect':0.8, 'smudged':0.1, 'black':0.1})
		else:
			return DDist({'perfect':0.1, 'smudged':0.7, 'black':0.2})
	
	def transitionModel(input):
		def transitionGivenInput(oldState):
			if oldState == 'good':
				return DDist({'good':0.7, 'bad':0.3})
			else:
				return DDist({'good':0.1, 'bad':0.9})
		return transitionGivenInput
			
	copyMachine = SSM(prior,transitionModel,observationModel)
	copyEstimator = SSE(copyMachine)
	
	copyMachine.start()
	copyEstimator.start()
	
	for n in range(20):
		
		observation = copyMachine.step("copy")
		print "Copy machine => ", observation
		belief = copyEstimator.step(observation)
		print "Estimate of copier's status: \n", belief.output(),"\n\n"
	
#============================MAIN==============================

def main():


	testSuite_SSE()		
	print "Program complete."
	
	
#This will run the testing suite if the program is run directly	
if __name__ == '__main__':
	main()