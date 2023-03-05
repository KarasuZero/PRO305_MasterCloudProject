import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "DELETE_Delete_Store":
        return delete_store(data)

def delete_store(data):
    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if store exists
        store_name = data['store_name']
        if cu.check_if_store_exists(store_name):

            # check if user is the owner of the store
            if cu.check_if_user_is_owner(username, store_name):

                # check password
                password = data['password']
                if cu.check_is_user(username, password):
                    # all checks passed
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # deleting store from Store_Table
                    Store_Table.delete_item(Key={'store_name': store_name})

                    # deleting store from Proprietor_Table
                    Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
                    Proprietor_Table.update_item(
                        Key={'username': username, 'password': password},
                        UpdateExpression="REMOVE properties[0]",
                        ConditionExpression="contains(properties, :i)",
                        ExpressionAttributeValues={
                            ':i': store_name
                        }
                    )

                    # generating response
                    body = {"message": "Store Deleted", "store_name": store_name}
                    return cu.create_response(200, body)

                else:
                    # generating response
                    return cu.create_response(400, "Invalid username or password")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")

    else:
        # generating response
        return cu.create_response(400, "User does not exist")