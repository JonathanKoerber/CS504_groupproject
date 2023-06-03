from flask import current_app, request
from twilio.rest import Client


def _get_twilio_verity_client():
    return Client(
        current_app.config["TWILIO_ACCOUNT_SID"],
        current_app.config["TWILIO_AUTH_TOKEN"],
    ).verify.services(current_app.config["TWILIO_VERIFY_SERVICE_ID"])


def request_verification_token(phone_number, channel="sms"):
    print(phone_number, channel)
    try:
        return _get_twilio_verity_client().verifications.create(
            to=phone_number,
            channel=channel,
        )
    except Exception as e:
        return e


def check_verification_token(phone_number, token):
    try:
        return _get_twilio_verity_client().verification_checks.create(
            to=phone_number, code=token
        )
    except Exception as e:
        print("error check verification token", e)
        return e
