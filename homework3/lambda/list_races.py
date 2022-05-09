import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    
    # Get nome della gara dal DynamoDB tramite il suo ID
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('GareRegistrate')
    response = table.scan()
    resp = table.scan(ProjectionExpression="Id, RaceName, RaceDate, RacePlace")

    body = resp["Items"]

    return {
        'statusCode': 200,
        'body': body
    }