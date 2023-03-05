import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "PATCH_Modify_Cart":
        return patch_modify_cart(data)

def patch_modify_cart(data):
    username = data['username']
    password = data['password']

    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    User_Table = DynamoDB.Table("PRO305_User_Table")

    # check if user exists
    if cu.check_if_username_exists(username):

        if cu.check_is_user(username, password):
            response = User_Table.get_item(Key={'username': username, 'password': password})
            item = response['Item']


            if not cu.check_if_item_in_cart(username, password, data['item_id']):
                if int(data['quantity']) > 0:
                    item = {
                        "menu_id": data['menu_id'],
                        "item_id": data['item_id'],
                        "quantity": data['quantity']
                    }

                    # add item to Cart in User_Table
                    User_Table.update_item(
                        Key={'username': username, 'password': password},
                        UpdateExpression="set Cart = list_append(Cart, :i)",
                        ExpressionAttributeValues={
                            ':i': [item]
                        },
                    )

            else:

                temp_list = item['Cart']
                for product in temp_list:
                    if product['item_id'] == data['item_id']:

                        current_quantity = int(product['quantity'])
                        new_quantity = current_quantity + int(data['quantity'])

                        if new_quantity > 0:
                            product['quantity'] = str(new_quantity)
                        elif new_quantity <= 0:
                            temp_list.remove(product)

                User_Table.update_item(
                    Key={'username': username, 'password': password},
                    UpdateExpression="set Cart = :i",
                    ExpressionAttributeValues={
                        ':i': temp_list
                    },
                )

            # generate response
            response = User_Table.get_item(Key={'username': username, 'password': password})
            item = response['Item']
            cart = item['Cart']

            body = {"Cart": cart, "message": "Item quantity updated" }
            return cu.create_response(200, body)

        else:
            # generate response
            return cu.create_response(400, "Password is incorrect")

    else:
        # generate response
        return cu.create_response(400, "User does not exist")