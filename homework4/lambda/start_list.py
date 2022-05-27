import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    id = event['queryStringParameters']['id']
    category = event['queryStringParameters']['class']
    
    # Get nome della griglia di partenza dal DynamoDB tramite il suo ID
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('GrigliaPartenza')
    response = table.get_item(
    Key={
        'Id': id
    })
    event_name = response["Item"]["FileName"]

    bucket_name = "xmlrequests"
    s3_path = "test/" + event_name + ".xml"
    
    # Get file XML dal BucketS3 ed estrai le categorie
    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
    tree = ET.parse(s3_object['Body'])
    root = tree.getroot()
    c = []
    body = "Categoria " + category + " non trovata"
    for child in root.findall("./ClassStart"):
        if(child.find("./Class/Name").text == category):
            for person in child.findall("PersonStart"):
                f = person.find('Person/Name/Family').text
                g = person.find('Person/Name/Given').text
                p = f + " " + g
                c.append(p)
            # Gli atleti sono inseriti nel file XML per ordine di arrivo, se si volessero ordinare togliere il commento
            body = json.dumps(c)
    
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