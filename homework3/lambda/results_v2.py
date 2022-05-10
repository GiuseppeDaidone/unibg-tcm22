import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    id = event['queryStringParameters']['id']
    org = event['queryStringParameters']['organisation']
    
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
    
    # Get file XML dal BucketS3 ed estrai i club
    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
    tree = ET.parse(s3_object['Body'])
    root = tree.getroot()
    o = {}
    body = "Il club " + org + " non è stato trovato"
    for child in root.findall("./ClassResult"):
        for person in child.findall("PersonResult"):
            if(person.find("Organisation/Name").text == org):
                i = person.find("Person/Id").text
                f = person.find("Person/Name/Family").text
                o.update({i : f})
    body = json.dumps(o)
    
    return {
        'statusCode': 200,
        'body': body
    }