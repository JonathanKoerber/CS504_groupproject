"""
This will have the functions that will be use to send the 
multiathentication email to the user
"""
from api.data_model import User
from flask_mail import Message
import random
import re
import os



def salt_password(password):
    # for every 2 characters, insert #!
    iterations = 0
    password_array = []
    for char in password:
        iterations += 1
        password_array.append(char)
        if iterations % 2 == 0:
            password_array.append("#!")
    return "".join(password_array)


def validate_name(string):
    if User.query.filter_by(username=string).first():
        raise ValueError("Username already exists!")
    if len(string) <= 255:
        return True
    else:
        raise ValueError("username should not exceet 255 characters")


def validate_passowrd(string):
    if len(string) <= 255 and len(string) >= 6:
        return True
    else:
        raise ValueError(
            "username and password shoult not exceet 255 characters and be longer then 8"
        )


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.match(pattern, email)
    if match:
        return True
    else:
        raise ValueError("Invalid email address!")


def validate_phone_number(phone_number):
    """validate phone number 1 (555) 555-5555"""
    pattern = r"^\d{1}\s\(\d{3}\)\s\d{3}-\d{4}$"
    match = re.match(pattern, phone_number)
    if match:
        return True
    else:
        raise ValueError("Invalid phone number! Valid format: 1 (555) 555-5555")


# def send_pin_email(user):
#     pin = random.randint(1000, 9999)
#     msg = Message(
#         "Password Reset Request", sender="noreply@gmail.com", recipients=user.email
#     )
#    
#  msg.body = """Hi there {user.username},  \n Use the pin to login to your account \n
#                     {pin}
#         If you did not make this request than you can simply ignore this email and no change will be made. 
#         """
#     for v, i in enumerate(msg.body):
#         pass
#     mail.send(message=msg)
#     print("Email sent!")
#     return pin
