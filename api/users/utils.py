"""
multi-authentication email to the user.
the user will simultaneously receive a text message and an email
bearing the same 4 digit pin that will be randomly generated.
"""
import re
from api.data_model import User



def salt_password(password):
    """
    salt password to create added complexity
    # for every 2 characters, insert #!
    """
    iterations = 0
    password_array = []
    for char in password:
        iterations += 1
        password_array.append(char)
        if iterations % 2 == 0:
            password_array.append("#!")
    return "".join(password_array)

def unser_name_unqiue(username):
    """
    check that username is not taken
    """
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists!")
    return True

def validate_name(string):
    """
    check that username is not longer then 255
    """
    if len(string) <= 255:
        return True
    else:
        raise ValueError("username and password shoult not exceed 255 characters")


def validate_passowrd(string):
    """
    check that password is longer then 8 characters and not longer then 255
    """
    if len(string) <= 255 and len(string) >= 6:
        return True
    else:
        raise ValueError(
            "username and password shoult not exceet 255 characters and be longer then 8"
        )


def validate_email(email):
    """
    check that email in in corect form.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.match(pattern, email)
    if match:
        return True
    else:
        raise ValueError("Invalid email address!")

def validate_phone_number(number):
    """
    check that phone number in in corect form.
    1 (234) 567-8910
    """
    pattern = r"^\d{1} \(\d{3}\) \d{3}-\d{4}$"
    match = re.match(pattern, number)
    if match:   
        return True
    else:
        raise ValueError("Invalid phone number!")

# def send_pin_email(user):

#     pin = random.randint(1000, 9999)
#     msg = Message('Password Reset Request', sender='noreply@gmail.com', recipients=user.email)
#     msg.body ='''Hi there {user.username},  \n Use the pin to login to your account \n
#                     {pin}
#         If you did not make this request than you can simply ignore this email and no change will be made.
#         '''
#     for v, i in enumerate(msg.body):
#         pass
#     mail.send(message=msg)
#     print("Email sent!")
#     return pin
