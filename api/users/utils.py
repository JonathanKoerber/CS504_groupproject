'''
This will have the functions that will be use to send the 
multi-authentication email to the user.
the user will simultaneously receive a text message and an email
bearing the same 4 digit pin that will be randomly generated.
'''


from flask_mail import Message
import random
import re
import os
from api import mail



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


def validate_email(email):
    """
    The local part and the domain name can contain one or more dots,
    no two dots can appear consecutively the first and last characters
    in the local part and in the domain name should not be dots.
    :param email:
    :return: True if the email meets the standards of an approved email address.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    if match:
        return True
    else:
        raise ValueError("Invalid email address!")


    
def send_pin_email(user):
    
    pin = random.randint(1000, 9999)
    msg = Message('Password Reset Request', sender='noreply@gmail.com', recipients=user.email)
    msg.body ='''Hi there {user.username},  \n Use the pin to login to your account \n
                    {pin}
        If you did not make this request than you can simply ignore this email and no change will be made. 
        '''
    for v, i in enumerate(msg.body):
        pass
    mail.send(message=msg)
    print("Email sent!")
    return pin
