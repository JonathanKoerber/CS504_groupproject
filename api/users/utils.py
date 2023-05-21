'''
This will have the functions that will be use to send the 
multi-authentication email to the user.
the user will simultaneously receive a text message and an email
bearing the same 4 digit pin that will be randomly generated.
'''

import random
import re
from sqlalchemy import create_engine, text

import ssl
import smtplib
from email.message import EmailMessage

from my_password import my_login_password


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


def validate_string(string):
    """
    :param string: user input, this is either email or password
    :return: True if user input is below 256 characters.
    """
    if len(string) <= 255:
        return True
    else:
        raise ValueError("username and password should not exceed 255 characters")

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

def confirm_authentication(is_authenticated):
    """
    :return: True if authentication is successful and False if authentication fails.
    If authentication is successful, the user then gets sent a pin for MFA.
    """
    if is_authenticated:
        return True
    else:
        print("Invalid username or password!")
        return False

def compare_pin(sent_pin, user_provided_pin):
    """
    :param sent_pin: If user pin matches the pin that was sent to the
    user, the MFA was successful.
    :param user_provided_pin: pin user have entered to complete MFA
    """

    if user_provided_pin == sent_pin:
        print("Login successful!")
    else:
        raise ValueError("Invalid pin, try again")

def generate_pin():
    """
    :return: returns a randomly generated 4 digit pin for MFA.
    """
    pin = random.randint(1000, 9999)
    return pin

def send_email(destination_email, pin):
    """
    :param pin: to be sent to the user's email address
    :param destination_email: the email address of the logged-in user
    that will be used for MFA.
    :return:
    """

    source_email = 'godwintardzenyuy@gmail.com'
    source_password = my_login_password

    recipient_email = destination_email

    subject = "MFA code"
    body = f"MFA pin: {pin}"


    em = EmailMessage()
    em['From'] = source_email
    em['To'] = recipient_email

    em['Subject'] = subject

    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(source_email, source_password)
        smtp.sendmail(source_email, recipient_email, em.as_string())

def get_user_email(username):
    """
    :param username: use the user's username to obtain the email from the database.
    :return: user's email address
    """
    query = text("SELECT email FROM users WHERE username = :username")

    # Connect to the database and execute the query
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1:6603/CS_504_PROJECT ')
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username})

    user_email = result.scalar()
    return user_email

def is_account_created(username):
    # use the user's username to obtain the email from the database.
    query = text("SELECT email FROM users WHERE username = :username")

    # Connect to the database and execute the query
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1:6603/CS_504_PROJECT')
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username})

    user_email = [result.scalar()]
    count = len(user_email)
    if count > 0:
        return True
    else:
        return False


def get_user():
    # Get user input
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not validate_string(username) or not validate_string(password):
        raise ValueError("Username or password should not exceed 255 characters")

    #   Create SQL query to check the user's login credentials
    query = text("SELECT * FROM CS_504_PROJECT.users WHERE username = :username and password = :password")

    # Connect to the database and execute the query
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1:6603/CS_504_PROJECT')
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username, "password": password})

    # Check if user exist and password is correct
    if result.fetchone() is not None:
        print("Login successful!")
        # get_login(username)
    else:
        raise ValueError("Invalid username or password.")

    return username