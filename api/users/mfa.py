'''
Contains functions for sending and checking verification tokens
'''
from flask import current_app
from twilio.rest import Client
import twilio.base.exceptions


def _get_twilio_verity_client():
    """
    Returns a Twilio Verify client
    """
    return Client(
        current_app.config["TWILIO_ACCOUNT_SID"],
        current_app.config["TWILIO_AUTH_TOKEN"],
    ).verify.services(current_app.config["TWILIO_VERIFY_SERVICE_ID"])


def request_verification_token(phone_number, channel="sms"):
    """
    Sends a verification token to the given phone number
    """
    print(phone_number, channel)
    try:
        return _get_twilio_verity_client().verifications.create(
            to=phone_number,
            channel=channel,
        )
    except twilio.base.exceptions.TwilioException as twilio_error:
        print("Error checking verification token:", twilio_error)
        return twilio_error


def check_verification_token(phone_number, token):
    """
    Checks a verification token
    """
    try:
        return _get_twilio_verity_client().verification_checks.create(
            to=phone_number, code=token
        )
    except twilio.base.exceptions.TwilioException as twilio_error:
        print("Error checking verification token:", twilio_error)
        return twilio_error
