import json
from aws_lambda_powertools import Logger
import os
import time
import uuid
import boto3

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


@logger.inject_lambda_context
def handler(event, context):
    # validate and extract task description from request body
    try:
        body = json.loads(event['body'])
        if 'description' not in body:
            raise Exception("missing task 'description' in body request")
    except Exception:
        logger.exception("Validation Failed")
        return {
            "statusCode": 400
        }
    # the request is valid, proceed with task creation
    timestamp = str(time.time())
    item = {
        'id': str(uuid.uuid1()),
        'description': body['description'],
        'createdAt': timestamp,
    }
    # write the task to the database
    table.put_item(Item=item)
    # create the response
    response = {
        "statusCode": 200,
        "body": json.dumps(item),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    logger.debug("execution completed", extra=response)
    return response
