import base64 as b64
import random as ran
import json
import boto3 as bt3

def b64Encode(body_element):
    return b64.b64encode(body_element.encode('utf-8')).decode('utf-8')


# decode a base64 str into a str
def b64Decode(body_element):
    return b64.b64decode(body_element).decode('utf-8')


def create_response(statusCode, body):
    return {
        'statusCode': statusCode,
        'body': body
    }


def keyGen():
    Characters = "00112233445566778899abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    Chars = []

    Key = ""


    for i in range(12):

        Chars.append(ran.choice(Characters))


        Key = "".join(Chars)


    return Key

def check_if_username_exists(username):
    dynamodb = bt3.resource('dynamodb')
    Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")
    # check if username exist in table
    try:
        response = Registered_User_Table.get_item(Key={'username': username})
        if 'Item' in response:
            return True
        else:
            return False

    except Exception as e:
        return False


data = {
  "operation": "POST_Create_Proprietor",
  "data":{
    "username": "owner_01",
    "password": "root",
    "name": "bobu",
    "email": "test@email.com",
    "phone": "1234567890"
  }
}

print(b64Encode(json.dumps(data)))
