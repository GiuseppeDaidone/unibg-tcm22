import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    id = event['queryStringParameters']['id']
    file_name = parameter_validation(id)
    file_name = file_name + ".xml"
    
    # Carico il BucketS3
    bucket_name = "xmlrequests"
    s3_path = "test/" + file_name
    s3_client = boto3.client("s3")
    
    #print(bucket_name + " " + file_name + " " + s3_path)
    
    # Scarico il file
    s3_client.download_file(bucket_name, s3_path, '/tmp/{}'.format(file_name))
    body = "File XML richiesto scaricato"
    
    return {
        'statusCode': 200,
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