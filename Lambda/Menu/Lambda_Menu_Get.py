import custom_util as cu

def lambda_handler(event, context):
    operation = event['queryStringParameters']['operation']

    if operation == "GET_Get_Menu_Item":  # works
        return get_menu_item(event['queryStringParameters']['menu_id'], event['queryStringParameters']['item_id'])
    elif operation == "GET_Get_Menu":  # works
        return get_menu(event['queryStringParameters']['menu_id'])


def get_menu(menu_id):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data

    # find menu by id
    menu = Menu_Table.get_item(Key={'menu_id': menu_id})
    if menu is None:
        return cu.create_response(400, "Menu Not Found")
    # generate response
    body = {"message": "Menu Found", "data": menu}

    return cu.create_response(200, cu.json.dumps(body))


def get_menu_item(menu_id, item_id):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data]
    # check if menu exists
    menu = Menu_Table.get_item(Key={'menu_id': menu_id})['Item']
    if menu is None:
        return cu.create_response(400, "Menu Not Found")
    # find item in menu
    for item in menu['items']:
        if item['item_id'] == item_id:
            body = {"message": "Menu Item Found", "data": item}
            return cu.create_response(200, cu.json.dumps(body))

    return cu.create_response(400, "Menu Item Not Found")
