# -*- coding: cp936 -*-
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
            x.append(self.denominator.coeff(i))
        y=x[:]
        y.reverse()
        roots_list=poly.Polynomial(y).roots()
        return roots_list

    def poleMagnitudes(self):
        x=[]
        for i in self.poles():
            magnitudes=abs(i)
            x.append(magnitudes)
        return x

    def dominantPole(self):
        def k(a):
            return abs(a) 
        the_pole=util.argmax(self.poles(),k)
        return the_pole


    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    the_numerator=sf1.numerator*sf2.numerator
    the_denominator=sf1.denominator*sf2.denominator
    return SystemFunction(the_numerator,the_denominator)   #补全Cascade函数后，swLab05Work才能正常运行

def FeedbackSubtract(sf1, sf2):
    the_numerator=sf1.numerator*sf2.denominator
    the_denominator=sf1.numerator*sf2.numerator+sf1.denominator*sf2.denominator
    return SystemFunction(the_numerator,the_denominator)    

