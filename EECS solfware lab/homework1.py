import lib601.sm as sm

#以下是类定义部分

class BinaryOp:
    def __init__(self, left=0, right=0):
        self.left = left
        self.right = right
    def __str__(self):
        return self.opStr + '(' + str(self.left) + ','+str(self.right) + ')'
    
class Sum(BinaryOp):  
    opStr = 'Sum'
    def eval(self,env):
        if isinstance(self.left,Number):
            if isinstance(self.right,Number):
                return self.left.value+self.right.value
            elif isinstance(self.left,Number) and isinstance(self.right,Sum):
                return  self.left.value+Sum.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Prod):
                return self.left.value+Prod.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Diff):
                return self.left.value+Diff.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Quot):
                return self.left.value+Quot.eval(self.right,env)
        elif isinstance(self.left,Variable):
            if self.left.name in env:
                if isinstance(self.right,Number):
                    return env[self.left.name]+self.right.value
                elif isinstance(self.right,Sum):
                    return env[self.left.name]+Sum.eval(self.right,env)
                elif isinstance(self.right,Prod):
                    return env[self.left.name]+Prod.eval(self.right,env)
                elif isinstance(self.right,Diff):
                    return env[self.left.name]+Diff.eval(self.right,env)
                elif isinstance(self.right,Quot):
                    return env[self.left.name]+Quot.eval(self.right,env)
                elif isinstance(self.right,Variable):
                    return env[self.left.name]+env[self.right.name]
            else:
                return None
        else:
            return None
class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self,env):
        if isinstance(self.left,Number) and isinstance(self.right,Number):
            return self.left.value*self.right.value
        elif isinstance(self.left,Variable) and isinstance(self.right,Number):
            if self.left.name in env:
                return env[self.left.name]*self.right.value
            else:
                return None
        elif isinstance(self.left,Variable) and isinstance(self.right,Variable):
            if self.left.name in env and self.right.name in env:
                return env[self.left.name]*env[self.right.name]
            else:
                return None
        else:
            return None
        
class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self,env):
        if isinstance(self.left,Number) and isinstance(self.right,Number):
            return self.left.value % self.right.value
        elif isinstance(self.left,Variable) and isinstance(self.right,Number):
            if self.left.name in env:
                return env[self.left.name]%self.right.value
            else:
                return None
        elif isinstance(self.left,Variable) and isinstance(self.right,Variable):
            if self.left.name in env and self.right.name in env:
                return env[self.left.name]%env[self.right.name]
            else:
                return None
        else:
            return None
        
class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self,env):
        if isinstance(self.left,Number):
            if isinstance(self.right,Number):
                return self.left.value-self.right.value
            elif isinstance(self.left,Number) and isinstance(self.right,Sum):
                return  self.left.value-Sum.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Prod):
                return self.left.value-Prod.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Diff):
                return self.left.value-Diff.eval(self.right,env)
            elif isinstance(self.left,Nmuber) and isinstance(self.right,Quot):
                return self.left.value-Quot.eval(self.right,env)
        elif isinstance(self.left,Variable):
            if self.left.name in env:
                if isinstance(self.right,Number):
                    return env[self.left.name]-self.right.value
                elif isinstance(self.right,Sum):
                    return env[self.left.name]-Sum.eval(self.right,env)
                elif isinstance(self.right,Prod):
                    return env[self.left.name]-Prod.eval(self.right,env)
                elif isinstance(self.right,Diff):
                    return env[self.left.name]-Diff.eval(self.right,env)
                elif isinstance(self.right,Quot):
                    return env[self.left.name]-Quot.eval(self.right,env)
                elif isinstance(self.right,Variable):
                    return env[self.left.name]-env[self.right.name]
            else:
                return None
        else:
            return None
        
class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self,env):
        if isinstance(self.left,Variable) and isinstance(self.right,Number):
            env[self.left.name]=self.right.value
            return None
        elif isinstance(self.left,Variable) and isinstance(self.right,Sum):
            env[self.left.name]=Sum.eval(self.right,env)
        elif isinstance(self.left,Variable) and isinstance(self.right,Diff):
            env[self.left.name]=Diff.eval(self.right,env)
        elif isinstance(self.left,Variable) and isinstance(self.right,Prod):
            env[self.left.name]=Prod.eval(self.right,env)
        elif isinstance(self.left,Variable) and isinstance(self.right,Quot):
            env[self.left.name]=Quot.eval(self.right,env)
        else:
            pass
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    def eval(self,env):
        return self.value
             
class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    def eval(self,env):
        return env[self.name]

class Tokenizer(sm.SM): #step5 -->Tokenizing by State Machine
    def __init__(self):
        self.startState=' '  
    def getNextValues(self,state,inp):
        op = ['(', ')', '+', '-', '*', '/', '=', '', ' ']
        if state ==' ':
            return (inp,'')
        elif state not in op:
            if inp not in op:
                return (state+inp,'')
            else:
                return (inp,state)
        elif state in op:
            return (inp,state)
        else :
            return ('','')

##以上都是关于 Synax tree 和 Symbolic Calculator 的相关类定义

tokenizer=Tokenizer()    ##step6 --> 创造一个Tokenizer的实例并且删掉列表中的空字符串
tokenlist=tokenizer.transduce('(fred + george) ')
while '' in tokenlist:
    tokenlist.remove('')
##print tokenlist     ##当进行step6时，请取消此行注释，即可查看step6的完成结果
    



##以下是homework中定义的一些函数
    
def tokenize(s):     ##step1 --> 这是第一问的tokenizer
    special=['(', ')', '+', '-', '*', '/', '=']
    for i in s:
        if i in special:
            s=s.replace(i,' %s '%i) ##如果字符串中出现了special内的元素，则将该元素前后都加上空格,目的是能将这些运算符与变量或数字分隔开来
    tokens=s.split()                ##使用字符串的split方法，将字符串用空格符分隔成子串，然后放到一个列表中.
    return tokens

##str1='(1+((2*a)+3))'          
##the_token=tokenize(str1)   ##这三行代码是检测step1函数的运行结果，当进行step1时，请取消此行注释，即可在shell界面显示出标记完成后的序列
##print(the_token)



def parse(tokens): ##step2 -->  这是一个解析器，用于解析tokenizer标记后的序列
    oplist=['+','-','*','/']
    def parseExp(index):
        def numberTok(token):
            if 48<=ord(token[0])<=57: ##判断token是不是代表数字
                return True
            else:
                return False
        def variableTok(token):
            if 65<=ord(token[0])<=90 or 97<=ord(token[0])<=122: #判断token是不是代表字母
                return True
            else:
                return False
        if numberTok(tokens[index]): ##对数字进行解析，返回一个Number类的实例，同时索引+1
            number=Number(float(tokens[index]))
            index=index+1
            return (number,index)
        elif variableTok(tokens[index]): ##对字母进行解析，返回一个Variable类的实例，同时索引+1
            variable=Variable(tokens[index])
            index=index+1
            return (variable,index)
        elif tokens[index]=='(': ## 解析( expression op expression )这种形式,显然token为'(', 以下是token='('时的递归解析法
            (left,index)=parseExp(index+1) #解析索引为index+1时的token,通过parseExp的返回值获得一个left tree
            op=tokens[index] ## 获取操作符op,通过操作符op以及left tree和right tree来构建一个internal syntax tree instance
            (right,index)=parseExp(index+1)## 继续解析，通过parseExp的返回值获得一个 right tree
            if op=='+':
                op=Sum(left,right)
                index=index+1
                return(op,index)
            if op=='-':
                op=Diff(left,right)
                index=index+1
                return(op,index)
            if op=='*':
                op=Prod(left,right)
                index=index+1
                return(op,index)
            if op=='%':
                op=Quot(left,right)
                index=index+1
                return(op,index)
            if op=='=':
                op=Assign(left,right)
                index=index+1
                return(op,index)
        else:
            return('can not parse',0)
    (parsedExp, nextIndex) = parseExp(0) #开始递归
    return parsedExp

##str1='(1+((2*a)+3))'          
##the_token=tokenize(str1)
##parse(the_token)
##print(parse(the_token))   #这四行是检测parse函数（解析器）的运行效果，当进行step2时，请取消注释，即可在shell中打印出解析后的结果

   
def calcTest(): #step4  --> Symbolic Calculator
    inp=input('% ')
    the_token=tokenize(inp)
    the_parse=parse(the_token)
    evaluation=the_parse.eval(env)
    print(evaluation)
    print('  env=',env)
    calcTest()
    
##env={}
##calcTest()  #这两行代码是初始化环境environment,并且调用函数calcTest，当进行step4时，请取消此行注释，即可在shell界面进行交互   




