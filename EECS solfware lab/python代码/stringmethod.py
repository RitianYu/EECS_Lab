def rotate_word(str,n):
    strstr=''
    for i in str:
        value=ord(i)
        value+=n
        strstr+=chr(value)
    return strstr
        

print(rotate_word('cheer',7))
        
