import re
"""
string = "ciao simone c ci"

array = ['i\'m', 'f', "what's", 'spell', 'fire', 'noo', 'haha']

array = [word for word in array if len(word) > 1]
print(array)"""

"""for word in array:
    print(word)
    print(re.sub(r'\b\w{1,1}\b', '', word))"""

"""
array = ["what's", 'spell', 'fire', 'noo', 'haha', '0', '0000', '01', '01a', "-2523"]
no_integers = [word for word in array if not (word.isdigit() or word[0] == '-' and word[1:].isdigit())]
print(no_integers)"""
"""
array = ['go', 'get', 'simone', 'davide' ]
array.remove('i\'m')
array.remove('go')
array.remove('get')
print(array)"""
array = ['find', 'perfectly', 'normal', 'almost', 'love', 'hello', 'kitty', 'mom', 'think', "i'm", 'freak']
array = [word for word in array if word != "i'm"]
array = [word for word in array if word != "love"]
print(array)
