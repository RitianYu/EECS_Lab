import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

def BayesEvidence(stateDistribution,observationModel,obs):
    jointDis={}
    conditionDis={}
    for i in stateDistribution.d:
        jointDis[(i,obs)]=stateDistribution.prob(i)*observationModel(i).prob(obs)
    for i in stateDistribution.d:
        conditionDis[i]=jointDis[(i,obs)]/sum(jointDis.values())
    return dist.DDist(conditionDis)

def TotalProbability(conditionDistribution,transitionModel):
    stateDis={}
    for i in conditionDistribution.d:
        for k in transitionModel(i).d:
            incrDictEntry(stateDis,k,conditionDistribution.prob(i)*transitionModel(i).prob(k))
    return dist.DDist(stateDis)

class StateEstimator(sm.SM):
    def __init__(self, model):
        self.model = model
        self.startState = model.startDistribution

    def getNextValues(self, state, inp):
        (o, i) = inp
        sGo=BayesEvidence(state,self.model.observationDistribution, o)
        dSPrime=TotalProbability(sGo,self.model.transitionDistribution(i))
        return (dSPrime,dSPrime)
 
def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v
# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print cmse.transduce(obs)


