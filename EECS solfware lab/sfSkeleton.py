"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    def __init__(self, numeratorPoly, denominatorPoly):
        self.numerator = numeratorPoly
        self.denominator = denominatorPoly

    def poles(self):
        x=[]
        for i in range(3):
            x.append(self.denomiantor.coeff(i))
        y=x[:]
        y.reverse()
        roots_list=poly.Polynomial(y).roots()
        return roots_list

    def poleMagnitudes(self):
        x=[]
        for i in range(2):
            x.append(abs(self.poles[i]))
        return x

    def dominantPole(self):
        if abs(self.poles[0])>=abs(self.poles[1])
            return self.poles[0]
        else:
            return self.poles[1]
            
    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    pass

def FeedbackSubtract(sf1, sf2=None):
    return sf1/(sf1*sf2+1)

