import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = ('L','L','L','L')
   legalInputs=('takeNone','takeGoat','takeWolf','takeCabbage')
   def getNextValues(self, state, action):
      if state==('L','L','L','L'):
         if action=='takeGoat':
            return (('R','R','L','L'),('R','R','L','L'))
         else:
            return (state,state)
      elif state==('L','L','L','R'):
         if action=='takeGoat':
            return (('R','R','L','R'),('R','R','L','R'))
         elif action=='takeWolf':
            return (('R','L','R','R'),('R','L','R','R'))
         else:
            return (state,state)
      elif state==('L','L','R','L'):
         if action=='takeGoat':
            return (('R','R','R','L'),('R','R','R','L'))
         elif action=='takeCabbage':
            return (('R','L','R','R'),('R','L','R','R'))
         else:
            return (state,state)
      elif state==('L','L','R','R'):
         if action=='takeGoat':
            return (('R','R','R','R'),('R','R','R','R'))
         elif action=='takeNone':
            return (('R','L','R','R'))
         else:
            return (state,state)
      elif state==('L','R','L','L'):
         if action=='takeNone':
            return (('R','R','L','L'),('R','R','L','L'))
         elif action=='takeWolf':
            return (('R','R','R','L'),('R','R','R','L'))
         elif action=='takeCabbage':
            return (('R','R','L','R'),('R','R','L','R'))
         else:
            return (state,state)
      elif state==('R','R','L','L'):
         if action=='takeNone':
            return (('L','R','L','L'),('L','R','L','L'))
         elif action=='takeGoat':
            return (('L','L','L','L'),('L','L','L','L'))
         else:
            return (state,state)
      elif state==('R','R','L','R'):
         if action=='takeGoat':
            return (('L','L','L','R'),('L','L','L','R'))
         elif action=='takeCabbage':
            return (('L','R','L','L'),('L','R','L','L'))
         else:
            return (state,state)
      elif state==('R','R','R','L'):
         if action=='takeGoat':
            return (('L','L','R','L'),('L','L','R','L'))
         elif action=='takeWolf':
            return (('L','R','L','L'),('L','R','L','L'))
         else:
            return (state,state)
      elif state==('R','L','R','R'):
         if action=='takeNone':
            return (('L','L','R','R'),('L','L','R','R'))
         elif action=='takeWolf':
            return (('L','L','L','R'),('L','L','L','R'))
         elif action=='takeCabbage':
            return (('L','L','R','L'),('L','L','R','L'))
         else:
            return (state,state)
      elif state==('R','R','R','R'):
         return (state,state)
   def done(self, state):
      if state==('R','R','R','R'):
         return True
farmerGoatWolfCabbage=FarmerGoatWolfCabbage()
print search.smSearch(farmerGoatWolfCabbage,initialState=None,goalTest=None,maxNodes=10000,depthFirst=False,DP=True)
