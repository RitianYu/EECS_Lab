#------------------------SM.PY-------------------------------
#
# State Machine Library
#
# Description: This class gives the functionality to create
#   state machines and simple autonoma, as well as the ability 
#   to combine machines in more complex patterns
#
# Includes:
#
# Combinators:
#  - Feedback
#  - Cascade
#  - Parallel
#  - Conjoined Parallel
#  - Parallel Add
#
# Autonoma:
#  - Wire		- Delay			- Incrementor
#  - Adder		- Counter		- Gain
#  - Selector	- Accumulator
#------------------------------------------------------------

#..............
# Note that SM is only a superclass, it does not define startState or
# getNextValues, which are specific to each state machine
#..............
class SM:
	
	def start(self):
		self.state = self.startState
		
	def step(self, inp):
		(s, o) = self.getNextValues(self.state, inp)
		self.state = s
		return o
		
	def transduce(self, inputs, verbose=False):
		self.start()
		
		outputs = []
		
		for inp in inputs:
			if verbose==True:
				print 'State=[',self.state,'], Input=[',inp,']'
			
			outputs.append(self.step(inp))
				
			if verbose==True:
				print '-->Output[',outputs[-1],']'	
		
		return outputs

#========COMBINATOR CLASSES==========

#.............
#Basic Combination State Machine class for 2 SMs
#.............
class cSM(SM):
	
	def __init__(self, SM1, SM2):
		self.first = SM1
		self.second = SM2
		self.startState = (SM1.startState, SM2.startState)
		
	def start(self):
		self.first.start()
		self.second.start()
		self.state = self.startState	
		
	def step(self, inp):
		#Update self
		(s, o) = self.getNextValues(self.state, inp)
		self.state = s

		#Update constituent machines
		self.stepConstituents(inp)

		return o			

	def stepConstituents(self, inp):
		self.first.step(inp)
		self.second.step(inp)

#..............
# Puts two state machines in sequence, with the 1st's output
# becoming the 2nd's input and with that output as the combined
#..............
class Cascade(cSM):	
		
	def getNextValues(self, state, inp):
		(s1, s2) = self.state
		(newS1, o1) = self.first.getNextValues(s1, inp)
		(newS2, o2) = self.second.getNextValues(s2, o1)
		return((newS1, newS2), o2)
		
	def stepConstituents(self, inp):
		out = self.first.step(inp)
		self.second.step(out)
		
#.............
#Puts both state machines in parallel, taking one input and
#returning a tuple of the inputs combined
#.............
class Parallel(cSM):
	
	def getNextValues(self, state, inp):
		(s1, s2) = self.state
		(newS1, o1) = self.first.getNextValues(s1, inp)
		(newS2, o2) = self.second.getNextValues(s2, inp)
		return((newS1, newS2), (o1, o2))
		
#.............
#A variation of parallel, it takes two inputs and feeds them
#independently to the two machines
#.............
class Parallel2(cSM):
	
	def getNextValues(self, state, inp):
		(i1, i2) = inp
		(s1, s2) = self.state
		(newS1, o1) = self.first.getNextValues(s1, i1)
		(newS2, o2) = self.second.getNextValues(s2, i2)
		return((newS1, newS2), (o1, o2))
		
#.............
#Outputs the sum of the two constituent, parallel, machines
#.............
class ParallelAdd(cSM):
	
	def getNextValues(self, state, inp):
		(s1, s2) = self.state
		(newS1, o1) = self.first.getNextValues(s1, inp)
		(newS2, o2) = self.second.getNextValues(s2, inp)
		return((newS1, newS2), o1+o2)

#.............
#Feedback combinator that takes its last output as its next
#input. This one can be overridden by setting inp=something
#.............

class Feedback(SM):			#<---NOTE! This inherits from SM not cSM, because it has only one component
	
	startState = 0
	lastOutput = 0
	
	def __init__(self, innerMachine):
		self.machine = innerMachine
		self.startState = self.machine.startState
		
	def start(self):
		self.state = self.startState
		self.machine.start()
		
	def step(self, inp=None):
		if inp==None:
			inp = self.lastOutput
		
		(s, o) = self.getNextValues(self.state, inp)
		self.state = s
		self.lastOutput = o
		self.machine.step(inp)
		
		return o
		
	def getNextValues(self, state, inp):
		return self.machine.getNextValues(state, inp)
		
		

#==========BASIC AUTONOMA=============		
		
#..............
# Defines a SM whose output is the sum of all past inputs
#..............
class Accumulator(SM):
	
	def __init__(self, initialValue):
		self.startState = initialValue
	
	def getNextValues(self, state, inp):
		return(state+inp, state+inp)
#..............

#..............
# Defines an SM whose output is the last input
#..............
class Delay(SM):
	
	def __init__(self, initialValue=0):
		self.startState = initialValue
	
	def getNextValues(self, state, inp):
		return(inp, state)
#..............

#..............
# Defines an SM whose output is the input multiplied by the gain
#..............
class Gain(SM):
	
	startState = 0
	
	def __init__(self, gain=1):
		self.gainFactor = gain
	
	def getNextValues(self, state, inp):
		return(state, inp*self.gainFactor)
#..............

#..............
# Defines an SM who always outputs the kth input element
#..............
class Selector(SM):
	
	startState = 0
	
	def __init__(self, kth=0):
		self.k = kth
	
	def getNextValues(self, state, inp):
		return(0, inp[self.k])
#..............

#..............
# Defines an SM whose output is always ++ the input
#..............
class Incrementor(SM):
	
	startState = 0
	
	def __init__(self, initial=0):
		self.startState = initial
	
	def getNextValues(self, state, inp):
		return(state, inp+1)
#..............

#..............
# Defines an SM whose output is always +=n of the state
#..............
class Counter(SM):
	
	startState = 0
	count = 1
	
	def __init__(self, count=1, initial=0):
		self.startState = initial
		self.count = count
	
	def getNextValues(self, state, inp):
		return(state+self.count, state+self.count)
#..............

#..............
# Output is always the sum of all inputs
#..............
class Adder(SM):
	
	startState=0
	
	def getNextValues(self, state, inp):
		return(state, sum(inp))
#..............

#..............
# Output equals input in a wire
#..............
class Wire(SM):
	startState=0
	
	def getNextValues(self, state, inp):
		return(state, inp)
#..............

#=============================================================
#				MAIN FUNCTION & TESTING SUITE
#=============================================================
def testSuite(machine, msg="", stepVals=(10,11,12), transVals=(1,2,4,8,16), verbose=False):
	#This will run a simple test of the machine
	print msg, "Test..."
	
	machine.start()
		
	for s in stepVals:
		print machine.step(s)
		
	print machine.transduce(transVals, verbose)
	
	print "Test complete."
	
def testNTuples(machine, msg="", n=2, verbose=False):
	#This will run a test suite on a machine that accepts n-tuples as inputs
	
	unit = [i+1 for i in range(n)]
	stepVals = [[i*(x+1) for i in unit] for x in range(3)]
	
	testSuite(machine, msg, stepVals, stepVals, verbose)
	
def runAllTestSuites():
	#Accumulator Test
	a = Accumulator(100)
	testSuite(a, "Accumulator ")
	
	#Incrementor Test
	i = Incrementor()
	testSuite(i, "Incrementor")
	
	#Delay Test
	r = Delay()
	testSuite(r, "Delay ")
	
	#Gain Test
	g = Gain(10)
	testSuite(g, "Gain ")
	
	#Selector Test
	s = Selector(4)
	testNTuples(s, "Selector ", 6)
	#testSuite(s, "Selector ", ((1,2,3,4,5,6,7,8,9,10),(2,4,6,8,10),(3,6,9,12,15,18,21)), ((0,2,0,4,0,6,0,8,0,10),('2','4','6','8','10'),'abcdefghijk'))
	
	#Cascade Test
	r1 = Delay()
	r2 = Delay()
	c = Cascade(r1, r2)
	testSuite(c, "Cascade Delays ", (1,2,3,4,5,6,7,8,9,10,11,12,13))
	
	#Double Cascade Test --> NOTE this uses cascade from previous test!
	r3 = Delay()
	r4 = Delay()
	c2 = Cascade(r3, r4)
	cT = Cascade(c, c2)
	testSuite(cT, "4x Delays ", (1,2,3,4,5,6,7,8,9,10,11,12,13))
	
	#Parallel Test
	a1 = Accumulator(10)
	a2 = Accumulator(100)
	p = Parallel(a1, a2)
	testSuite(p, "Parallel Accumulators ")
	
	#Parallel2 Test
	a1 = Accumulator(0)
	a2 = Accumulator(0)
	p2 = Parallel2(a1, a2)
	testNTuples(p2, "Conjoined Accumulators ", 2, True)
	
	#ParallelAdd Test
	a1 = Accumulator(0)
	a2 = Accumulator(0)
	pA = ParallelAdd(a1, a2)
	testSuite(pA, "Summed Accumulators ", (10,11,12), (1,2,4,8,16), True)
	
	#Counter/Cascade Test
	c = Cascade(Counter(1), Delay(0))
	print "Counter "
	c.start()
	for count in range(10):
		print c.step(0)
		
	#Feedback Test
	f = Feedback(Gain(2))	
	print "Feedback Doubler"
	f.start()
	f.step(1)
	for count in range(10):
		print f.step()
		
	#Adder Test
	add = Adder()
	testNTuples(add, "Adder Machine ", 6, True)

def main():

	#runAllTestSuites()
	#Fibonacci Sequence
	
	fib = Feedback(Cascade(Parallel(Delay(1), Wire()), Adder()))
	fib.start()
	for count in range(10):
		print fib.step()
	
	
#This will run the testing suite if the program is run directly	
if __name__ == '__main__':
	main()
