import json
import xml.etree.ElementTree as ET
import boto3
import uuid
import string
import random

def lambda_handler(event, context):
    
    content = event["body"]
    race_name = event["headers"]["race_name"]
    race_date = event["headers"]["race_date"]
    race_place = event["headers"]["race_place"]
    email = event["headers"]["email"]
    encoded_string = content.encode("utf-8")
    assert check_xml(content)
    assert headers_validation(race_name, race_date, race_place, email)
    assert check_if_race_exists()
    assert check_if_user_exists()
    
    # Genero gli identificativi di gara e utente
    r = {}
    id = str(id_gen())
    token = token_gen()
    
    # Upload nel DynamoDB della gara registrata
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('GareRegistrate')
    item = {
        'Id': id,
        'RaceName': race_name,
        'RaceDate': race_date,
        'RacePlace': race_place,
        'Email': email
    }
    table.put_item(Item=item)
    
    # Upload nel DynamoDB del nuovo utente
    table = dynamo.Table('Amministratori')
    item = {
        'Token': token,
        'Email': email
    }
    table.put_item(Item=item)
    
    # Valori di ritorno
    r.update({id : token})
    body = json.dumps(r)
    
    return {
        'statusCode': 200,
        'body': body
    }

def headers_validation(race_name, race_date, race_place, email): # Check se header non sono vuoti
    return True
    
def check_if_race_exists(): # Check se la gara è stata già registrata
    return True

def check_if_user_exists(): # Check se l'utente è già stato registrato
    return True

def id_gen(): # Genero id univoco
    return uuid.uuid4()

def token_gen(): # Genero un token casuale di 24 caratteri (controllare se l'utente esiste già nel DynamoDB)
    token = string.ascii_lowercase
    return ''.join(random.choice(token) for i in range(24))