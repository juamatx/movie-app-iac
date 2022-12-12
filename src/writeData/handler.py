import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

with open('./movies.json', 'r') as myfile:
    data = myfile.read()
movie_list = json.loads(data)


def handler(event, context):
    for movie in movie_list:
        response = table.put_item(
            Item={
                'id': movie['id'],
                'movieName': movie['movieName'],
                'movieOfTheWeek': movie['movieOfTheWeek'],
                'alreadyPicked': movie['alreadyPicked'],

            }
        )
