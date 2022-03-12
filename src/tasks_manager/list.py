import json
import os
from aws_lambda_powertools import Logger
from src.tasks_manager import decimalencoder
import boto3

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

DEFAULT_PAGE_LIMIT = 10


@logger.inject_lambda_context
def handler(event, context):
    # extract optional pagination parameters from the request
    query_string_params = event.get('queryStringParameters', dict())
    limit = int(query_string_params.get('limit', DEFAULT_PAGE_LIMIT))
    next_page = query_string_params.get('nextPage')
    # prepare scan request parameters
    scan_params = {
        "Limit": limit
    }
    if next_page:
        scan_params["ExclusiveStartKey"] = {
            "id": next_page
        }
    # retrieve a page of tasks from the table
    result = table.scan(**scan_params)
    # create the response
    response = {
        "statusCode": 200,
        "body": json.dumps(
            {
                "tasks": result['Items'],
                "size": result['Count'],
                "next_page": result.get('LastEvaluatedKey', dict()).get("id")
            },
            cls=decimalencoder.DecimalEncoder),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    logger.debug("execution completed", extra=response)
    return response
