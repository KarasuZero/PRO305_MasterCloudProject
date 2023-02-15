import custom_util as cu


#Example regisred user table json
# {
#  username: "test",
#  password: "test", #### im not sure if we want to store the password in the table
#  cart: [
#   {
#     item_id: "1",
#     quantity: 1
#    },
#    {
#     item_id: "2",
#     quantity: 1
#    }
#  ]
# }

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']
    
    if operation == "PUT_Add_To_Cart":
        return put_add_to_cart(data)
    if operation == "PUT_Remove_From_Cart":
        return put_remove_from_cart(data)
    if operation == "Get_Cart":
        return get_cart(data)
    
    def put_add_to_cart (data):
        # dynamodb stuff
        dynamodb = cu.bt3.resource("dynamodb")
        User_Table = dynamodb.Table('PRO305_Registered_User_Table')
        Menu_Table = dynamodb.Table('PRO305_Menu_Table')
        
        # grabbing username and item
        username = data['username']
        menu_id = data['menu_id']
        item_id = data['item_id']
        item_found = False
        
        #check if item exists in menu
        menu = Menu_Table.get_item(Key={'menu_id': menu_id})['Item']
        if menu is None: 
            return cu.create_response(400, "Menu does not exist")
        #find item in menu
        for item in menu['items']:
            if item['item_id'] == item_id:
                item_to_add = item
                break
        if item_to_add is None:
            return cu.create_response(400, "Item does not exist")
        #check if item is already in cart
        user = User_Table.get_item(Key={'username': username})['Item']
        for item in user['Cart']:
            if item['item_id'] == item_id:
                #increment quantity
                item_found = True
                item['quantity'] += 1
                break
        if not item_found:
            #add item to cart
            user['Cart'].append(item_to_add)
        #update user table
        User_Table.put_item(Item=user)
        #generate response
        return cu.create_response(200, cu.json.dumps(user['Cart']))
    def put_remove_from_cart (data):
        # dynamodb stuff
        dynamodb = cu.bt3.resource("dynamodb")
        User_Table = dynamodb.Table('PRO305_Registered_User_Table')
        Menu_Table = dynamodb.Table('PRO305_Menu_Table')
        
        # grabbing username and item
        username = data['username']
        menu_id = data['menu_id']
        item_id = data['item_id']
        item_found = False
        
        #check if item exists in menu
        menu = Menu_Table.get_item(Key={'menu_id': menu_id})['Item']
        if menu is None: 
            return cu.create_response(400, "Menu does not exist")
        #find item in menu
        for item in menu['items']:
            if item['item_id'] == item_id:
                item_to_remove = item
                break
        if item_to_remove is None:
            return cu.create_response(400, "Item does not exist")
        #check if item is already in cart
        user = User_Table.get_item(Key={'username': username})['Item']
        for item in user['Cart']:
            if item['item_id'] == item_id:
                #decrement quantity
                item_found = True
                item['quantity'] -= 1
                if item['quantity'] == 0:
                    user['Cart'].remove(item)
                break
        if not item_found:
            #item not in cart
            return cu.create_response(400, "Item not in cart")
        #update user table
        User_Table.put_item(Item=user)
        #generate response
        return cu.create_response(200, cu.json.dumps(user['Cart']))
    def get_cart (data):
        # dynamodb stuff
        dynamodb = cu.bt3.resource("dynamodb")
        User_Table = dynamodb.Table('PRO305_Registered_User_Table')
        
        # grabbing username
        username = data['username']
        
        #check if user exists
        user = User_Table.get_item(Key={'username': username})['Item']
        if user is None: 
            return cu.create_response(400, "User does not exist")
        #generate response
        return cu.create_response(200, cu.json.dumps(user['Cart']))
               
        
