import turtle
import math
bob=turtle.Turtle()

def umbrella2(n,r):
    beta=180/n
    radian_beta=beta*math.pi/180
    d=r*math.sin(radian_beta)*2

    for i in range(n):
        bob.lt(beta)
        bob.fd(r)
        bob.rt(beta + 90)
        bob.fd(d)
        bob.rt(beta+90)
        bob.fd(r)
        bob.rt(180+beta)



umbrella2(5,100)


