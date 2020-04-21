import hashlib
from random import choice, randint


def coder(resp):
    cs = resp.encoding
    return resp.text.encode(cs).decode('utf8')
	
def get_userNameAndPassword():
    char ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = "1234567890"
    e_userName = []
    e_userPassword = []
    for i in range(randint(4, 7)):
        e_userName.append(choice(char))
    for j in range(randint(3, 6)):
        e_userName.append(choice(num))
    for m in range(5):
        e_userPassword.append(choice(char))
    for n in range(7):
        e_userPassword.append(choice(num))
    userName = ''.join(e_userName)
    userPassword = ''.join(e_userPassword)
    print("userName:", userName)
    print("userPassword:", userPassword)
    return userName,  userPassword

def md5(raw):
    return hashlib.md5(raw.encode('utf8')).hexdigest()
	
def format_data_or_headers(string):
    print(dict([item.split(': ') for item in string.split('\n') if item]))