import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    id = event['queryStringParameters']['id']
    
    # Get nome della gara dal DynamoDB tramite il suo ID
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('RisultatiGare')
    response = table.get_item(
    Key={
        'Id': id
    })
    event_name = response["Item"]["Evento"]

    bucket_name = "xmlrequests"
    s3_path = "test/" + event_name + ".xml"
    
    # Get file XML dal BucketS3 ed estrai le categorie
    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
    tree = ET.parse(s3_object['Body'])
    root = tree.getroot()
    categories = {}
    for child in root.iter('Class'):
        i = child.find('Id').text
        categories.update({i : child.find('Name').text})
    body = json.dumps(categories)
    
    
    return {
        'statusCode': 200,
        'body': body
    }