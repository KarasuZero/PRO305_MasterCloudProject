import custom_util as cu
from uuid import uuid4

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
    if operation == "GET_Get_Menu":
        return get_menu(data)
    if operation == "PUT_Add_Menu_Item":
        return put_add_menu_item(data)
    if operation == "DELETE_Delete_Menu_Item":
        return delete_menu_item(data)
    if operation == "DELETE_Delete_Menu":
        return delete_menu(data)
    if operation == "GET_Get_All_Menus":
        return cu.get_all_content_from_table("PRO305_Menu_Table")
    
   # elif operation == "DELETE_Delete_Menu_Item":
       # return delete_menu_item(data)

def get_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    
    #find menu by id
    menu = Menu_Table.get_item(Key={'id': id})
    if menu is None:
        return cu.create_response(400, "Menu Not Found")
    #generate response
    body = {"message": "Menu Found" , "data": menu}
    
    return cu.create_response(200, cu.json.dumps(body))
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
    menu = Menu_Table.get_item(Key={'id': id, 'item_id': item_id})
    
    #edit item
    if name is not None:
        menu['name'] = name
    if price is not None:
        menu['price'] = price
    if description is not None:
        menu['description'] = description
    
                
    #update item object in menu table
    Menu_Table.update_menu( 
        Key={'id': id},
        UpdateExpression="set items = :i",
        ExpressionAttributeValues={
            ':i': menu['items']
        }
    )
    
    #this is code i researched and found online, i will test it later
    Menu_Table.update_item(
        Key={'id': id, 'item_id': item_id},
        UpdateExpression= "set items = :i",
        ExpressionAttributeValues={
            ':i': menu
        }    
    )
    #update item
    body = {"message": "Menu Item Updated" , "data": menu}
    
    return cu.create_response(200, cu.json.dumps(body))
def post_create_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = str(uuid4())
    item_id = str(uuid4())
    items = data['items']
    #insert into Menu_Table
    Menu_Table.put_item(Item={
        "id": id,
        "items": [
            {
                "item_id": item_id
            }
        ]
    })
    
    body = {"message": "Menu Created" , "data": data}
    
    return cu.create_response(200, cu.json.dumps(body))

def get_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')
    
    #grabbing data
    id = data['id']
    item_id = data['item_id']
    body = Menu_Table.get_item(Key={'id': id, 'item_id': item_id})
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
    response = Menu_Table.delete_item(Key={'id': id, 'item_id': item_id})
    
    body = {"message": "Menu Item Deleted", "data": response}
    
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