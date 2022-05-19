import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    #content = event["body"]
    id = event['queryStringParameters']['id']
    file_name = parameter_validation(id)
    file_name = file_name + ".xml"
    
    # Carico il BucketS3
    bucket_name = "xmlrequests"
    s3_path = "test/" + file_name
    s3_client = boto3.resource("s3")
    
    # Scarico il file
    s3_object = s3_client.Object(bucket_name, s3_path)
    body = s3_object.get()['Body'].read().decode('utf-8') 
    
    return {
        'statusCode': 200,
        'headers': {
          "Access-Control-Allow-Origin": "*", # Required for CORS support to work
          "Access-Control-Allow-Credentials": "true", # Required for cookies, authorization headers with HTTPS
          "Access-Control-Allow-Headers": "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale",
          "Access-Control-Allow-Methods": "GET"
        },
        'body': body
    }

def parameter_validation(id): # Check se l'id corrisponde
    event = ""
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('RisultatiGare')
    response = table.get_item(
    Key={
        'Id': id
    })
    event = response["Item"]["Evento"]
    return event

def find_xml(): # Da implementare
    return True