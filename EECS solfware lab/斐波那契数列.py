def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    elif n>1:
        return fib(n-1)+fib(n-2)
    else:
        return False

print(fib(-1))
for i in range(10):
    print(fib(i))


  
