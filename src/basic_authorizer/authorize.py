from aws_lambda_powertools import Logger
import os
from base64 import b64encode

logger = Logger()

BASIC_AUTH_USERNAME = os.environ['BASIC_AUTH_USERNAME']
BASIC_AUTH_PASSWORD = os.environ['BASIC_AUTH_PASSWORD']


@logger.inject_lambda_context
def handler(event, context):
    # extract request authorization header
    request_authorization_header = event.get("headers", dict()).get("authorization", "")
    # compute the valid authorization header
    authorization_secret = b64encode(
        f"{BASIC_AUTH_USERNAME}:{BASIC_AUTH_PASSWORD}".encode()
    ).decode()
    valid_authorization_header = f"Basic {authorization_secret}"
    # check validity of the request provided
    if request_authorization_header == valid_authorization_header:
        is_authorized = True
    else:
        is_authorized = False
    # create response
    response = {
        "isAuthorized": is_authorized,
    }
    logger.debug(f"authorizer response", extra=response)
    return response
