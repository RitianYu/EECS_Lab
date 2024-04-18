cube=float(input('请输入任意的cube值\n'))
if abs(cube) < 1:
    num = len(str(abs(cube))) - 1
    cube_ = abs(cube) * (10 ** (num-1) )
def cube_root(x):
    epsilon=0.01
    low=0
    high=abs(x)
    guess=(high+low)/2.0
    cube_ = abs(x)
    while abs(guess**3-abs(x))>=epsilon:
        if guess ** 3 < cube_:
            low = guess
        else:
            high = guess
        guess = (high + low) / 2.0
    return guess
if  cube>=1 or cube==0:
    print(num_guess)
    print(cube_root(cube),'is close to the cube root of',cube)
elif 0<cube<1:
    print(cube_root(cube_)/cube_root(10 ** (num-1)),'is close to the cube root of',cube)
elif -1<cube<0:
    print(-cube_root(cube_)/cube_root(10 ** (num-1)), 'is close to the cube root of', cube)
else:
    print(cube_root(cube), 'is close to the cube root of', cube)

