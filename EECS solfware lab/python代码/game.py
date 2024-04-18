
def is_abecedarian(word):
    word.lower()
    for index in range(len(word)):
        if index==len(word)-1:
            break
        if not word[index]<=word[index+1]:
            return False
    return True
print(is_abecedarian('cbadfe'))
    
def use_only(word,str):
    for letter in word:
        if letter not in str:
            return False
    return True

def use_all(word,str):
    return use_only(str,word)

print(use_all('love','alove'))
