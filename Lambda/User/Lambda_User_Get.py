import custom_util as cu

def lambda_handler(event, context):
    operation = event['queryStringParameters']['operation']

    if operation == "GET_All_Store":
        return get_all_store()

    elif operation == "GET_Store":
        return get_store(event['queryStringParameters']['store_name'])

    elif operation == "GET_Menu_By_ID":
        return get_menu_by_id(event['queryStringParameters']['menu_id'])

    elif operation == "GET_Menu_By_Name":
        return get_menu_by_name(event['queryStringParameters']['store_name'])


def get_all_store():
    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    Store_Table = DynamoDB.Table("PRO305_Store_Table")

    # scan table
    response = Store_Table.scan()

    # grab items
    items = response['Items']

    # generate response
    return cu.create_response(200, cu.json.dumps(items))

def get_store(store_name):
    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    Store_Table = DynamoDB.Table("PRO305_Store_Table")

    # check if store exists
    if cu.check_if_store_exists(store_name):
        # get item
        response = Store_Table.get_item(Key={'store_name': store_name})
        item = response['Item']

        # generate response
        return cu.create_response(200, item)

    else:
        # generate response
        return cu.create_response(400, "Store does not exist")

def get_menu_by_id(menu_id):
    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    Menu_Table = DynamoDB.Table("PRO305_Menu_Table")

    # check if menu exists
    if cu.check_if_menu_exists(menu_id):
        # get item
        response = Menu_Table.get_item(Key={'menu_id': menu_id})
        item = response['Item']

        # generate response
        return cu.create_response(200, cu.json.dumps(item))

    else:
        # generate response
        return cu.create_response(400, "Menu does not exist")


def get_menu_by_name(store_name):
    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    Store_Table = DynamoDB.Table("PRO305_Store_Table")

    # check if store exists
    if cu.check_if_store_exists(store_name):
        # get item
        response = Store_Table.get_item(Key={'store_name': store_name})
        item = response['Item']

        new_list = []

        # for each menu in menu_list
        for menu_id in item['menu_list']:
            new_list.append(get_menu_by_id(menu_id))

        # generate response
        return cu.create_response(200, new_list)

    else:
        # generate response
        return cu.create_response(400, "Store does not exist")