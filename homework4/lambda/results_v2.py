import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
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
    o = []
    body = "Il club " + org + " non è stato trovato"
    for child in root.findall("./ClassResult"):
        for person in child.findall("PersonResult"):
            try:
                node = person.find("Organisation/Name")
                if(node.text == org):
                    f = person.find("Person/Name/Family").text
                    g = person.find("Person/Name/Given").text
                    t = person.find("Result/Time").text
                    p = {}
                    p.update({"Name": g})
                    p.update({"Surname": f})
                    p.update({"Time": t})
                    o.append(p)
            except AttributeError:
                continue
                
    body = json.dumps(o)
    
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