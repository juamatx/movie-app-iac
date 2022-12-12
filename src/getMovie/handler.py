import boto3
from boto3.dynamodb.conditions import Attr
import os

# Resource

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def getMovieOfTheWeek():

    data = table.scan(FilterExpression=Attr('movieOfTheWeek').eq(True))

    if data:
        return data['Items'][0]['movieName']
    else:
        return ""


def handler(event, context):

    return getMovieOfTheWeek()
