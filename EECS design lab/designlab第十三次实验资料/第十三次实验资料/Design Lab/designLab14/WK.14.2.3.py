import lib601.util as util

class MyClass:
    def __init__(self, v):
        self.v = v 


def lotsOfClass1(n, v):
    one = MyClass(v)
    result = []
    for i in range(n):
        result.append(one)
    return result

def lotsOfClass2(n,v):
    result=[]
    for i in range(n):
        result.append(MyClass(v))
    return result

def lotsOfClass3(n,v):
    def f(n):
        return MyClass(v)
    return util.makeVectorFill(n,f)

def lotsOfClass4(n,v):
    return util.makeVector(n,MyClass(v))

class10=lotsOfClass3(10,'oh')
class10[0].v='no'


