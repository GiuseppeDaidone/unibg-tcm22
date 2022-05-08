import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    # Carico il BucketS3
    bucket_name = "xmlrequests"
    file_name = "Example event_gara.xml"
    s3_path = "test/" + file_name
    
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket("xmlrequests")
    
    s3_client = boto3.client("s3")
    files = {}
    body = ""
    
    # Per ogni file all'interno del BucketS3
    for object in my_bucket.objects.all():
        # Carico il file
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=object.key)
        # Estraggo le categorie dal file XML
        tree = ET.parse(s3_object['Body'])
        root = tree.getroot()
        categories = {}
        for child in root.iter('Class'):
            i = child.find('Id').text
            categories.update({i : child.find('Name').text})
        files = json.dumps(categories)
        body = body + files + "\n"
    
    return {
        'statusCode': 200,
        'body': body
    }
