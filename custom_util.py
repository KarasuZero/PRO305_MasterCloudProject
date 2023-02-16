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
        print("error: ")
        print(e)
        return False


def check_is_user(username, password):
    dynamodb = bt3.resource('dynamodb')
    Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")
    User_Table = dynamodb.Table("PRO305_User_Table")
    Proprietor_Table = dynamodb.Table("PRO305_Proprietor_Table")
    # check if user exist in table
    try:
        response = Registered_User_Table.get_item(Key={'username': username})
        if 'Item' in response:
            if response['Item']['role'] == 'PROPRIETOR':
                # check password
                print("Proprietor")
                try:
                    response = Proprietor_Table.get_item(Key={'username': username, 'password': password})
                    if 'Item' in response:
                        return True
                    else:
                        return False

                except Exception as e:
                    print("error: ")
                    print(e)
                    return False

            elif response['Item']['role'] == 'USER':
                # check password
                print("User")
                try:
                    response = User_Table.get_item(Key={'username': username, 'password': password})
                    if 'Item' in response:
                        return True
                    else:
                        return False

                except Exception as e:
                    print("error: ")
                    print(e)
                    return False
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
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
        print("error: ")
        print(e)
        return False


def check_if_store_exists(store_name):
    dynamodb = bt3.resource('dynamodb')
    Store_Table = dynamodb.Table("PRO305_Store_Table")
    # check if store exist in table
    try:
        response = Store_Table.get_item(Key={'store_name': store_name})
        if 'Item' in response:
            return True
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False


def check_if_user_is_owner(username, store_name):
    dynamodb = bt3.resource('dynamodb')
    Store_Table = dynamodb.Table("PRO305_Store_Table")
    # check if store exist in table
    try:
        response = Store_Table.get_item(Key={'store_name': store_name})
        if 'Item' in response:
            if response['Item']['proprietor'] == username:
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False


def get_all_content_from_table(table_name):
    dynamodb = bt3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.scan()

    return response.get('Items', [])


def check_if_menu_exists(menu_id):
    dynamodb = bt3.resource('dynamodb')
    Menu_Table = dynamodb.Table("PRO305_Menu_Table")
    # check if menu exist in table
    try:
        response = Menu_Table.get_item(Key={'menu_id': menu_id})
        if 'Item' in response:
            return True
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False


def check_if_menu_in_store(menu_id, store_name):
    dynamodb = bt3.resource('dynamodb')
    Store_Table = dynamodb.Table("PRO305_Store_Table")

    # check if store exist in table
    try:
        response = Store_Table.get_item(Key={'store_name': store_name})
        if 'Item' in response:
            temp_list = response['Item']['menu_list']
            if menu_id in temp_list:
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False

def check_if_item_in_menu(menu_id, item_id):
    # dynamodb stuff
    dynamodb = bt3.resource('dynamodb')
    Menu_Table = dynamodb.Table("PRO305_Menu_Table")

    # check if menu exist in table
    try:
        response = Menu_Table.get_item(Key={'menu_id': menu_id})
        if 'Item' in response:
            item_list = response['Item']['items']
            for item in item_list:
                if item['item_id'] == item_id:
                    return True

                else:
                    return False
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False

def check_if_item_in_cart(username, password, item_id):
    # dynamodb stuff
    dynamodb = bt3.resource('dynamodb')
    User_Table = dynamodb.Table("PRO305_User_Table")

    # check if menu exist in table
    try:
        response = User_Table.get_item(Key={'username': username, "password": password})
        if 'Item' in response:
            item_list = response['Item']['Cart']
            for item in item_list:
                if item['item_id'] == item_id:
                    return True

                else:
                    return False
        else:
            return False

    except Exception as e:
        print("error: ")
        print(e)
        return False


# json data to be sent to lambda
data = {
  "operation": "PATCH_Modify_Cart",
  "data":{
    "username": "user_01",
    "password": "user_01_pass",
    "menu_id": "570a76f6-b324-4b74-91d0-4bdfe952d119",
    "item_id": "1e60aea5-c71d-49ee-ac8a-97fb6d1cee69",
    "quantity": "-3"
  }
}

# data encoded using base64
print("encoded data:\n")
print(b64Encode(json.dumps(data)))

# data decoded using base64 ( debug )
# print("decoded data:\n")user
# print(b64Decode(b64Encode(json.dumps(data))))
