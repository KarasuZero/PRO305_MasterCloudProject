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


def check_is_user(username, password):
    dynamodb = bt3.resource('dynamodb')
    User_Table = dynamodb.Table("PRO305_User_Table")
    # check if user exist in table
    try:
        response = User_Table.get_item(Key={'username': username})
        if 'Item' in response:
            if response['Item']['password'] == password:
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        return False


def check_if_user_is_proprietor(username):
    dynamodb = bt3.resource('dynamodb')
    Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")
    # check if user exist in table
    try:
        response = Registered_User_Table.get_item(Key={'username': username})

        if 'Item' in response:

            # check if user is proprietor
            if response['Item']['role'] == 'PROPRIETOR':
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        return False

def check_if_store_exists(store_name):
    dynamodb = bt3.resource('dynamodb')
    Store_Table = dynamodb.Table("PRO305_Store_Table")
    # check if store exist in table
    try:
        response = Store_Table.get_item(Key={'storename': store_name})
        if 'Item' in response:
            return True
        else:
            return False

    except Exception as e:
        return False

def check_if_user_is_owner(username, store_name):
    dynamodb = bt3.resource('dynamodb')
    Store_Table = dynamodb.Table("PRO305_Store_Table")
    # check if store exist in table
    try:
        response = Store_Table.get_item(Key={'storename': store_name})
        if 'Item' in response:
            if response['Item']['proprietor'] == username:
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        return False

def get_all_content_from_table(table_Name):
    dynamodb = bt3.resource('dynamodb')
    table = dynamodb.Table(table_Name)

    response = table.scan()

    return response.get('Items', [])


# json data to be sent to lambda
data = {

}

# data encoded using base64
print("encoded data:\n")
print(b64Encode(json.dumps(data)))

# data decoded using base64 ( debug )
# print("decoded data:\n")
# print(b64Decode(b64Encode(json.dumps(data))))

# retrieving data from dynamodb
table_name = "PRO305_Registered_User_Table"
print(get_all_content_from_table(table_name))

