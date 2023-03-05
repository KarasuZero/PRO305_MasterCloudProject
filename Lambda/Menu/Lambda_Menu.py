import custom_util as cu
from uuid import uuid4


# Menu Table Example Json
# { "id": "2983Jdd233hd",
#  "items": [
#  {
#     "item_id": "2983Jdd233hd",
#    "name": "Cheeseburger",
#    "price": 5.99,
#   "description": "A delicious cheeseburger"
#  },
# {
# "item_id": "298373jihid322",
# "name": "Hamburger",
# "price": 4.99,
# "description": "A delicious hamburger"
# }
# ]
# }
#


def lambda_handler(event, context):
    
    if event['body'] == "" or event["body"] is None:
        operation = event['queryStringParameters']['operation']
        
        if operation == "GET_Get_Menu_Item":  # works
            return get_menu_item(event['queryStringParameters']['menu_id'], event['queryStringParameters']['item_id'])
        elif operation == "GET_Get_Menu":  # works
            return get_menu(event['queryStringParameters']['menu_id'])
    

    if event['queryStringParameters'] == {} or event['queryStringParameters'].get('authorizationToken'):
        # decode b64
        decoded_body = cu.b64Decode(event['body'])
        loaded_body = cu.json.loads(decoded_body)

        # grabbing operation and data
        operation = loaded_body['operation']
        data = loaded_body['data']

        # passing data to the correct method base on op
        if operation == "PUT_Edit_Menu_Item":  # works
            return put_edit_menu_item(data)  # if you use put you do not have to do a patch for each attribute you can replace the whole item
        elif operation == "POST_Create_Menu":  # works
            return post_create_menu(data)
        elif operation == "PUT_Add_Menu_Item":  # works
            return put_add_menu_item(data)
        elif operation == "PUT_Delete_Menu_Item":  # works
            return put_delete_menu_item(data)
        elif operation == "DELETE_Delete_Menu":  # works
            return delete_menu(data)


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


def put_edit_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = data['menu_id']
    item_id = data['item_id']
    # if data exsit grab it if not set it to none
    if 'name' in data and data['name'] != "":
        name = data['name']
    else:
        name = None
    if 'price' in data and data['price'] != "":
        price = data['price']
    else:
        price = None
    if 'description' in data and data['description'] != "":
        description = data['description']
    else:
        description = None

    # get menu from menu table find the item within the items array and update it
    menu = Menu_Table.get_item(Key={'menu_id': id})['Item']
    if menu is None:
        return cu.create_response(400, "Menu Not Found")
    for item in menu['items']:
        if item['item_id'] == item_id:
            if name is not None:
                item['name'] = name
            if price is not None:
                item['price'] = price
            if description is not None:
                item['description'] = description

    # update
    Menu_Table.put_item(Item=menu)
    # update item
    body = {"message": "Menu Item Updated", "data": menu}

    return cu.create_response(200, cu.json.dumps(body))


def post_create_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = str(uuid4())
    data['menu_id'] = id
    items = data['items']

    # for each item in items array add item_id
    for item in items:
        item_id = str(uuid4())
        item['item_id'] = item_id
    # insert into Menu_Table
    Menu_Table.put_item(Item=data)

    body = {"message": "Menu Created", "data": data}

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


def put_add_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = data['menu_id']
    item_id = str(uuid4())
    name = data['name']
    price = data['price']
    description = data['description']

    # find menu by id
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    menu = Menu_Table.get_item(Key={'menu_id': id})["Item"]
    # add item to menu
    menu['items'].append({
        "item_id": item_id,
        "name": name,
        "price": price,
        "description": description
    })

    body = {"message": menu}

    Menu_Table.put_item(Item=menu)
    return cu.create_response(200, cu.json.dumps(body))


def put_delete_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    item_id = data['item_id']
    id = data['menu_id']

    menu = Menu_Table.get_item(Key={'menu_id': id})["Item"]
    for item in menu['items']:
        if item['item_id'] == item_id:
            menu['items'].remove(item)
            Menu_Table.put_item(Item=menu)
            return cu.create_response(200, "Menu Item Deleted")
    return cu.create_response(200, "Menu Item Not Found")


def delete_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = data['menu_id']

    # delete menu
    Menu_Table.delete_item(Key={'menu_id': id})

    body = {"message": "Menu Deleted"}

    return cu.create_response(200, cu.json.dumps(body))
