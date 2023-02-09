import custom_util as cu

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
   # elif operation == "DELETE_Delete_Menu_Item":
       # return delete_menu_item(data)
    
def patch_edit_menu_item(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Store_Table = dynamodb.Table("PRO305_Store_Table")
    
    #grabbing data
    store_id = data['store_id']
    item_id = data['item_id']
    name = data['name']
    price = data['price']
    description = data['description']
    
    #find menu item by id
    store = Store_Table.get_item(Key={'store_id': store_id})
    
    #find menu item by id in the store
    for item in store['Item']['menu']:
        #if item found then edit it
        if item['item_id'] == item_id:
            if name != "":
                item['name'] = name
            if price != "":
                item['price'] = price
            if description != "":
                item['description'] = description
    #update store
    Store_Table.put_item(Item=store['Item'])
    body = {"message": "Menu Item Updated"}
    
    return cu.create_response(200, cu.json.dumps(body))

    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    