import os
from aws_lambda_powertools import Logger
import boto3

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


@logger.inject_lambda_context
def handler(event, context):
    # extract task id param from the request
    task_id = event.get('pathParameters', dict()).get('id')
    if task_id is None:
        # missing task id in the request
        status_code = 400
    else:
        # deleting task_id from the database
        table.delete_item(
            Key={
                'id': task_id
            }
        )
        status_code = 202
    # create the response
    response = {
        "statusCode": status_code
    }
    logger.debug("execution completed", extra=response)
    return response
