class V2:
    def  __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return 'V2[%g,%g]'%(self.x,self.y)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def add(self,other):
        self.x=self.x+other.x
        self.y=self.y+other.y
        return self
    def mul(self,scalar):
        self.x=self.x*scalar
        self.y=self.y*scalar
        return self
    def __add__(self,other):
        return self.add(other)  
    def __mul(self,scalar):
        return self.mul(other)

print(V2(1.1, 2.2))
v = V2(1.0, 2.0)
print(v.getX())
print(v.getY())
a = V2(1.0, 2.0)
b = V2(2.2, 3.3)
print(a.add(b))
print(a.mul(2))
print(a.add(b).mul(-1))
print(V2(1.1, 2.2) + V2(3.3, 4.4))