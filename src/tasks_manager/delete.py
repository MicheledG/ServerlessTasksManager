import os

import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def delete(event, context):
    # delete the task from the database
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
