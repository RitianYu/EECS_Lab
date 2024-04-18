def first(word):
    return word[0]
def last(word):
    return word[-1]
def middle(word):
    return word[1:-1]
def is_palindrome(str):
    if str=='' :
        return True
    else:
        if first(str)==last(str) or len(str)==1:
            return is_palindrome(middle(str))
        else:
            return False

if is_palindrome('wooow'):
    print('回文')
else:
    print('不是回文')
