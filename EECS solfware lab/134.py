# procedure tokenize
def tokenize(s):
    sequence=[]
    a=[]
    special=['(', ')', '+', '-', '*', '/', '=']
    for i in s:
        if not i==' ':
            if i in special:
                sequence.append(''.join(a))
                sequence.append(i)
                a=[]
            else:
                a.append(i)
    return sequence
print(tokenize('((fred + george) / (voldemort + 666))'))

