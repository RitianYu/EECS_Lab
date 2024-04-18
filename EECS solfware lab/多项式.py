from decimal import Decimal
from math import sqrt
class Polynomial:
    coeffs=[]
    def __init__(self,coefficients):
        self.coeffs=coefficients
        
    def coeff(self,i):
        coefficient_i=self.coeffs[i]
        return coefficient
    
    def add(self,other):
        sum=Polynomial([])
        small=Polynomial([])
        o_list=[]
        if len(self.coeffs)>len(other.coeffs):
            sum.coeffs=self.coeffs[:]
            for i in range(len(self.coeffs)-len(other.coeffs)):
                o_list=o_list+[0]
                small.coeffs=o_list+other.coeffs
            for i in range(len(self.coeffs)):
                sum.coeffs[i]=self.coeffs[i]+small.coeffs[i]
        elif len(self.coeffs)<len(other.coeffs):
            sum.coeffs=self.coeffs[:]
            for i in range(len(other.coeffs)-len(self.coeffs)):
                o_list=o_list+[0]
                small.coeffs=o_list+self.coeffs
            for i in range(len(self.coeffs)):
                sum.coeffs[i]=other.coeffs[i]+small.coeffs[i]
        else:
            sum.coeffs=self.coeffs[:]
            sum.coeffs[i]=self.coeffs[i]+other.coeffs[i]
        return sum
    
    def __str__(self):
        z=self.coeffs[:]
        z[-1]=str(self.coeffs[-1])
        if self.coeffs[-2]==0:
            z[-2]=''
        else:
            z[-2]=str(self.coeffs[-2])+'z'
        if len(self.coeffs)>=3 :
            for i in range(3,len(self.coeffs)+1):
                if self.coeffs[-i]==0:
                    z[-i]=''
                else:
                    z[-i]=str(self.coeffs[-i])+'z**'+str(i-1)
        return '+'.join(z)
    
    def val(self,v):
        s=self.coeffs[-1]
        for i in range(2,len(self.coeffs)+1):
            s=s+self.coeffs[-i]*v**(i-1)
        return s
    
    def mul(self,other):
        mul_=Polynomial([])
        mul2=Polynomial([])
        mul3=Polynomial([])
        mul_.coeffs=[0]*(len(self.coeffs)+len(other.coeffs)-1)
        mul2.coeffs=[0]*(len(self.coeffs)+len(other.coeffs)-1)
        mul3.coeffs=[0]*(len(self.coeffs)+len(other.coeffs)-1)
        for i in range(1,len(other.coeffs)+1):
            for j in range(1,len(self.coeffs)+1):
                mul_.coeffs[-(i+j-1)]=other.coeffs[-i]*self.coeffs[-j]
        for i in range(1,len(self.coeffs)+1):
            for j in range(1,len(other.coeffs)+1):
                mul2.coeffs[-(i+j-1)]=other.coeffs[-j]*self.coeffs[-i]       
        for i in range(len(mul_.coeffs)):
            if  mul_.coeffs[i]==mul2.coeffs[i]:
                mul3.coeffs[i]=mul_.coeffs[i]
            else:
                mul3.coeffs[i]=mul_.coeffs[i]+mul2.coeffs[i]
        return mul3
    
    def roots(self):
        if len(self.coeffs)>3 or len(self.coeffs)==1 :
            print('error!I can not handle it!')
        if len(self.coeffs)==2:
            root=-self.coeffs[1]/self.coeffs[0]
            return [root]
        elif len(self.coeffs)==3:
            a=self.coeffs[0]
            b=self.coeffs[1]
            c=self.coeffs[2]
            p=-b/(2*a)
            if b**2-4*a*c>=0:
                delta=(b**2-4*a*c)**0.5
                q=delta/(2*a)
            else:
                print(p)
                delta=complex(b**2-4*a*c,0)**0.5
                q=delta/(2*a)
            return [p+q,p-q]                  
        else: 
            print('error!I can not handle it!')
            
p1=Polynomial([1,2,3])
p2=Polynomial([100,200])
p3=Polynomial([3,2,-1])
print(p1)
print(p2)
print(p1.val(1))
print(p1.mul(p2))
