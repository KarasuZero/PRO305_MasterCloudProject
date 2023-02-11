import custom_util as cu

   #Menu Table Example Json
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
    #decode b64
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)
    
    #grabbing opperation and data
    operation = loaded_body['operation']
    data = loaded_body['data']
    
    #passing data to the correct method base on op
    if operation == "PATCH_Edit_Menu_Item":
        return patch_edit_menu_item(data)
    if operation == "POST_Create_Menu":
        return post_create_menu(data) 
    if operation == "GET_Get_Menu_Item":
        return get_menu_item(data)
    if operation == "PUT_Add_Menu_Item":
        return put_add_menu_item(data)
    if operation == "DELETE_Delete_Menu_Item":
        return delete_menu_item(data)
    if operation == "DELETE_Delete_Menu":
        return delete_menu(data)
    
   # elif operation == "DELETE_Delete_Menu_Item":
       # return delete_menu_item(data)
    
def patch_edit_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    item_id = data['item_id']
    name = data['name']
    price = data['price']
    description = data['description']
    
    #find menu by id and retreive item to be edited
    menu = Menu_Table.get_item(Key={'id': id})
    #look for correct item in menu
    for item in menu['items']:
        if item['item_id'] == item_id:
            if name != "":
                item['name'] = name
            if price != "":
                item['price'] = price
            if description != "":
                item['description'] = description
    #update item object in menu table
    #this is code i researched and found online, i will test it later
    Menu_Table.update_menu( 
        Key={'id': id},
        UpdateExpression="set items = :i",
        ExpressionAttributeValues={
            ':i': menu['items']
        },
        ReturnValues="UPDATED_NEW"
    )
    
    #update item
    body = {"message": "Menu Item Updated"}
    
    return cu.create_response(200, cu.json.dumps(body))
def post_create_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    items = data['items']
    
    #insert into Menu_Table
    Menu_Table.put_item(Item={
        "id": id,
        "items": items
    })
    
    body = {"message": "Menu Created"}
    
    return cu.create_response(200, cu.json.dumps(body))
def get_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    item_id = data['item_id']
    #find menu item by id
    menu = Menu_Table.get_item(Key={'id': id})
    for menu_item in menu['items']:
        if menu_item['item_id'] == item_id:
            body = menu_item
            return cu.create_response(200, cu.json.dumps(body))
def put_add_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    item_id = data['item_id']
    name = data['name']
    price = data['price']
    description = data['description']
     
    
    #find menu by id
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    menu = Menu_Table.get_item(Key={'id': id})
    #add item to menu
    menu['items'].append({
        "item_id": item_id,
        "name": name,
        "price": price,
        "description": description
    })
    
    body = {"message": menu}
    return cu.create_response(200, cu.json.dumps(body))
def delete_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    item_id = data['item_id']
    
    #find menu by id
    menu = Menu_Table.get_item(Key={'id': id})
    #find item in menu
    for menu_item in menu['items']:
        if menu_item['item_id'] == item_id:
            #remove item from menu
            menu['items'].remove(menu_item)
    #update menu
    Menu_Table.update_menu( 
        Key={'id': id},
        UpdateExpression="set items = :i",
        ExpressionAttributeValues={
            ':i': menu['items']
        },
        ReturnValues="UPDATED_NEW"
    )
    
    body = {"message": "Menu Item Deleted"}
    
    return cu.create_response(200, cu.json.dumps(body))
def delete_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    
    #delete menu
    Menu_Table.delete_item(Key={'id': id})
    
    body = {"message": "Menu Deleted"}
    
    return cu.create_response(200, cu.json.dumps(body))

    
    
    



    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    