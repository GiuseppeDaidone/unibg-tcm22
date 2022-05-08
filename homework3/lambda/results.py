import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    id = event['queryStringParameters']['id']
    category = event['queryStringParameters']['class']
    
    # Get nome della gara dal DynamoDB tramite il suo ID
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('ReportGare')
    response = table.get_item(
    Key={
        'Id': int(id)
    })
    event_name = response["Item"]["Evento"]

    bucket_name = "xmlrequests"
    s3_path = "test/" + event_name + ".xml"
    
    # Get file XML dal BucketS3 ed estrai le categorie
    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
    tree = ET.parse(s3_object['Body'])
    root = tree.getroot()
    c = {}
    body = "Categoria " + category + " non trovata"
    for child in root.findall("./ClassResult"):
        if(child.find("./Class/Id").text == category):
            body = "OK"
            for person in child.findall("PersonResult"):
                i = person.find('Result/Position').text
                c.update({i : person.find('Person/Name/Given').text})
            #c = dict(sorted(c.items())) ordinamento che funziona male :(
            body = json.dumps(c)
    
    return {
        'statusCode': 200,
        'body': body
    }