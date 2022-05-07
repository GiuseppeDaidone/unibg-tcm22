import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    header = event["headers"]["id"]
    encoded_string = content.encode("utf-8")
    assert check_xml(content)
    assert header_validation(header)
    
    # Upload del file XML nel BucketS3 con un nome temporaneo
    bucket_name = "xmlrequests"
    file_name = "tmp_gara.xml"
    s3_path = "test/" + file_name
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    
    # Upload nel DynamoDB degli IDEventi
    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
    tree = ET.parse(s3_object['Body'])
    root = tree.getroot()
    name_root = root.find('Event')
    name_event = name_root.find('Name').text
    date_event = name_root.find('./StartTime/Date').text
    xml_name = name_event + " " + date_event
    xml_name = xml_name.replace(" ", "_")
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('ReportGare')
    item = {
        'Id': int(header),
        'Evento': xml_name
    }
    table.put_item(Item=item)
    # Elimina il file XML temporaneo dal BucketS3
    s3 = boto3.resource("s3")
    s3.Object(bucket_name, s3_path).delete()
    
    # Upload del file XML nel BucketS3 in via definitiva
    file_name = xml_name + ".xml"
    s3_path = "test/" + file_name
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    body = "Caricamento del file \'" + xml_name + ".xml\' effettuato con successo"
    
    return {
        'statusCode': 200,
        'body': body
    }
    
def check_xml(content):
    return True
    
def header_validation(header):
    return True