import boto3
import json
import os
from boto3.dynamodb.conditions import Attr
import random
import time

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)
neverPickedMovies = table.scan(
    FilterExpression=Attr('alreadyPicked').eq(False))['Items']

currentMovie = table.scan(FilterExpression=Attr('movieOfTheWeek').eq(True))


def getCurrentMovieId(currentMovieV):
    return currentMovieV['Items'][0]['id']


def returnRandomMovie():
    return random.choice(neverPickedMovies)


def chooseNewMovieOfTheWeek():

    # Movie of the week, no longer is movieOfTheWeek
    updateCurrentMovie()
    time.sleep(2)

    # A random movie becomes the new movieOfTheWeek
    # alreadyPicked is set to True, for tracking purposes
    table.update_item(Key={'id': returnRandomMovie()['id']},
                      UpdateExpression='set alreadyPicked =:S, movieOfTheWeek=:N',
                      ExpressionAttributeValues={":S": True, ":N": True})


def updateCurrentMovie():
    # Movie of the week, no longer is movieOfTheWeek
    table.update_item(Key={'id': currentMovie['Items'][0]['id']},
                      UpdateExpression='set movieOfTheWeek =:S',
                      ExpressionAttributeValues={":S": False})


def handler(event, context):

    chooseNewMovieOfTheWeek()
