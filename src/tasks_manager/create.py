import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def handler(event, context):
    data = json.loads(event['body'])
    if 'description' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
    
    timestamp = str(time.time())

    item = {
        'id': str(uuid.uuid1()),
        'description': data['description'],
        'createdAt': timestamp,
    }

    # write the task to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
