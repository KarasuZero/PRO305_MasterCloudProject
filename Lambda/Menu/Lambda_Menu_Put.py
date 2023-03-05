import custom_util as cu
from uuid import uuid4

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "PUT_Edit_Menu_Item":  # works
        return put_edit_menu_item(data)  # if you use put you do not have to do a patch for each attribute you can replace the whole item
    elif operation == "PUT_Add_Menu_Item":  # works
        return put_add_menu_item(data)
    elif operation == "PUT_Delete_Menu_Item":  # works
        return put_delete_menu_item(data)


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