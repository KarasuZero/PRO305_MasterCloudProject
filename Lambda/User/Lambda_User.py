import custom_util as cu


# Example registered user table json
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

# def lambda_handler(event, context):
#
#     # check if body is empty
#     if event['body'] == "":
#         # grabbing op
#         operation = event['queryStringParameters']['operation']
#
#         if operation == "GET_All_Store":
#             return get_all_store()
#
#         elif operation == "GET_Store":
#             return get_store(event['queryStringParameters']['store_name'])
#
#         elif operation == "GET_Menu_By_ID":
#             return get_menu_by_id(event['queryStringParameters']['menu_id'])
#
#         elif operation == "GET_Menu_By_Name":
#             return get_menu_by_name(event['queryStringParameters']['store_name'])
#
#     elif event['queryStringParameters'] == {} or event['queryStringParameters'].get('authorizationToken'):
#         # grab body and do b64 stuff
#         decoded_body = cu.b64Decode(event['body'])
#         loaded_body = cu.json.loads(decoded_body)
#
#         # grabbing op and data
#         operation = loaded_body['operation']
#         data = loaded_body['data']
#
#         if operation == "POST_Get_Cart":
#             return post_get_cart(data)
#         elif operation == "PATCH_Modify_Cart":
#             return patch_modify_cart(data)
#         elif operation == "POST_Checkout":
#             return post_checkout(data)
#
#
# def get_all_store():
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     Store_Table = DynamoDB.Table("PRO305_Store_Table")
#
#     # scan table
#     response = Store_Table.scan()
#
#     # grab items
#     items = response['Items']
#
#     # generate response
#     return cu.create_response(200, items)
#
#
# def get_store(store_name):
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     Store_Table = DynamoDB.Table("PRO305_Store_Table")
#
#     # check if store exists
#     if cu.check_if_store_exists(store_name):
#         # get item
#         response = Store_Table.get_item(Key={'store_name': store_name})
#         item = response['Item']
#
#         # generate response
#         return cu.create_response(200, item)
#
#     else:
#         # generate response
#         return cu.create_response(400, "Store does not exist")
#
#
# def get_menu_by_id(menu_id):
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     Menu_Table = DynamoDB.Table("PRO305_Menu_Table")
#
#     # check if menu exists
#     if cu.check_if_menu_exists(menu_id):
#         # get item
#         response = Menu_Table.get_item(Key={'menu_id': menu_id})
#         item = response['Item']
#
#         # generate response
#         return cu.create_response(200, item)
#
#     else:
#         # generate response
#         return cu.create_response(400, "Menu does not exist")
#
#
# def get_menu_by_name(store_name):
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     Store_Table = DynamoDB.Table("PRO305_Store_Table")
#
#     # check if store exists
#     if cu.check_if_store_exists(store_name):
#         # get item
#         response = Store_Table.get_item(Key={'store_name': store_name})
#         item = response['Item']
#
#         new_list = []
#
#         # for each menu in menu_list
#         for menu_id in item['menu_list']:
#             new_list.append(get_menu_by_id(menu_id))
#
#         # generate response
#         return cu.create_response(200, new_list)
#
#     else:
#         # generate response
#         return cu.create_response(400, "Store does not exist")


# def post_get_cart(data):
#     username = data['username']
#     password = data['password']
#
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     User_Table = DynamoDB.Table("PRO305_User_Table")
#
#     # check if user exists
#     if cu.check_if_username_exists(username):
#
#         # check password
#         if cu.check_is_user(username, password):
#             # get item
#             response = User_Table.get_item(Key={'username': username, 'password': password})
#             item = response['Item']
#
#             # generate response
#             return cu.create_response(200, item['Cart'])
#
#         else:
#             # generate response
#             return cu.create_response(400, "Password is incorrect")
#
#     else:
#         # generate response
#         return cu.create_response(400, "User does not exist")


# def patch_modify_cart(data):
#     username = data['username']
#     password = data['password']
#
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     User_Table = DynamoDB.Table("PRO305_User_Table")
#
#     # check if user exists
#     if cu.check_if_username_exists(username):
#
#         if cu.check_is_user(username, password):
#             response = User_Table.get_item(Key={'username': username, 'password': password})
#             item = response['Item']
#
#
#             if not cu.check_if_item_in_cart(username, password, data['item_id']):
#                 if int(data['quantity']) > 0:
#                     item = {
#                         "menu_id": data['menu_id'],
#                         "item_id": data['item_id'],
#                         "quantity": data['quantity']
#                     }
#
#                     # add item to Cart in User_Table
#                     User_Table.update_item(
#                         Key={'username': username, 'password': password},
#                         UpdateExpression="set Cart = list_append(Cart, :i)",
#                         ExpressionAttributeValues={
#                             ':i': [item]
#                         },
#                     )
#
#             else:
#
#                 temp_list = item['Cart']
#                 for product in temp_list:
#                     if product['item_id'] == data['item_id']:
#
#                         current_quantity = int(product['quantity'])
#                         new_quantity = current_quantity + int(data['quantity'])
#
#                         if new_quantity > 0:
#                             product['quantity'] = str(new_quantity)
#                         elif new_quantity <= 0:
#                             temp_list.remove(product)
#
#                 User_Table.update_item(
#                     Key={'username': username, 'password': password},
#                     UpdateExpression="set Cart = :i",
#                     ExpressionAttributeValues={
#                         ':i': temp_list
#                     },
#                 )
#
#             # generate response
#             response = User_Table.get_item(Key={'username': username, 'password': password})
#             item = response['Item']
#             cart = item['Cart']
#
#             body = {"Cart": cart, "message": "Item quantity updated" }
#             return cu.create_response(200, body)
#
#         else:
#             # generate response
#             return cu.create_response(400, "Password is incorrect")
#
#     else:
#         # generate response
#         return cu.create_response(400, "User does not exist")


# def post_checkout(data):
#     username = data['username']
#     password = data['password']
#
#     # dynamoDB stuff
#     DynamoDB = cu.bt3.resource("dynamodb")
#     User_Table = DynamoDB.Table("PRO305_User_Table")
#
#     # check if user exists
#     if cu.check_if_username_exists(username):
#
#         if cu.check_is_user(username, password):
#             response = User_Table.get_item(Key={'username': username, 'password': password})
#             item = response['Item']
#
#             # grab email
#             email = item['email']
#
#             # grab name
#             name = item['name']
#
#             # send cart to sqs
#             cu.send_cart(username, password, email, name)
#
#             # generate response
#             return cu.create_response(200, "Order placed")
#
#
#         else:
#             # generate response
#             return cu.create_response(400, "Password is incorrect")
#
#     else:
#         # generate response
#         return cu.create_response(400, "User does not exist")
