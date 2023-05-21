'''
This will have the functions that will be use to send the 
multiathentication email to the user
'''

import re

def salt_password(password):
    # for every 2 characters, insert #!
    iterations = 0
    password_array = []
    for char in password:
        iterations += 1
        password_array.append(char)
        if iterations % 2 == 0:
            password_array.append('#!')
    return ''.join(password_array)

def validate_name(string):
    if len(string) <= 255:
        return True
    else:
        raise ValueError("username and password shoult not exceet 255 characters")
def validate_passowrd(string):
        if len(string) <= 255 and len(string) >= 6:
            return True
        else:
            raise ValueError("username and password shoult not exceet 255 characters and be longer then 8")

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' 
def validate_email(email):
    
    match = re.match(pattern, email)
    if match:
        return True
    else:
        raise ValueError("Invalid email address!")