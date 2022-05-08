import json
import xml.etree.ElementTree as ET
import boto3
import uuid

def lambda_handler(event, context):
    
    content = event["body"]
    id = event["headers"]["id"]
    token = event["headers"]["token"]
    encoded_string = content.encode("utf-8")
    assert check_xml(content)
    assert headers_validation(id, token)
    
    # Get utente dal DynamoDB tramite il suo token
    email = find_user(token)
    if(email != ""):
        # Upload del file XML nel BucketS3 con un nome temporaneo
        bucket_name = "xmlrequests"
        file_name = "tmp_gara.xml"
        s3_path = "test/" + file_name
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
        
        # Upload nel DynamoDB della gara
        s3 = boto3.client("s3")
        s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path)
        tree = ET.parse(s3_object['Body'])
        root = tree.getroot()
        name_root = root.find('Event')
        name_event = name_root.find('Name').text
        print(id + " " + token)
        name = find_name(id, email)
        if(name == name_event):
            date_event = name_root.find('./StartTime/Date').text
            xml_name = name_event + " " + date_event
            xml_name = xml_name.replace(" ", "_")
            dynamo = boto3.resource('dynamodb')
            table = dynamo.Table('RisultatiGare')
            item = {
                'Id': id,
                'Evento': xml_name,
                'CaricatoDa': email
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
        else:
            # Elimina il file XML temporaneo dal BucketS3
            s3 = boto3.resource("s3")
            s3.Object(bucket_name, s3_path).delete()
            
            body = "La gara che si vuole caricare non è stata ancora registrata"
    else:
        body = "Utente inesistente"
    
    return {
        'statusCode': 200,
        'body': body
    }
    
def check_xml(content): # Check se rispetta il DTD
    return True
    
def headers_validation(id, token): # Check se header non sono vuoti
    return True
    
def find_user(token): # Cerca se l'utente che sta caricando la gara è presente tra gli amministratori
    email = ""
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('Amministratori')
    response = table.get_item(
    Key={
        'Token': token
    })
    email = response["Item"]["Email"]
    return email
    
def find_name(id, email): # Cerca se la gara del file XML è già stata registrata
    name = ""
    print(id)
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('GareRegistrate')
    response = table.get_item(
    Key={
        'Id': id
    })
    name = response["Item"]["RaceName"]
    return name