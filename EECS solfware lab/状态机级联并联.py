import lib601.sm as sm

class BA1(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        if inp != 0:
            newState = state * 1.02 + inp - 100
        else:
            newState = state * 1.02
        return (newState, newState)

class BA2(sm.SM):
    startState = 0
    def getNextValues(self, state, inp):
        newState = state * 1.01 + inp
        return (newState, newState)

class PureFunction(sm.SM):
    def __init__(self,f):
        self.startState=f
    def getNextValues(self,state,inp):
        return (state,state(inp))

def the_max(x):
    if x[0]>=x[1]:
        return x[0]
    else :
        return x[1]

def the_sum(inp):
    return inp[0]+inp[1]

ba1=BA1()
ba2=BA2()
purefunction1=PureFunction(the_max)
purefunction2=PureFunction(the_sum)
maxAccount=sm.Cascade(sm.Parallel(ba1,ba2),purefunction1)  ## 最大化-->状态机实例
switchAccount=sm.Cascade(sm.Parallel2(ba1,ba2),purefunction2) ## 投资-->状态机实例



####以下命令在shell中输入

##maxAccount.start()
##maxAccount.step(input)  #第一个input是一个数值
##switchAccount.start()
##switchAccount.step(input) #第二个input是包含两个数值的元组

###在shell中对两个类实例使用start方法以及step方法，即可得到不同存款金额下的问题1和问题2的输出结果

