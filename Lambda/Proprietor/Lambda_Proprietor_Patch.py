import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "PATCH_Transfer_Ownership":
        return patch_transfer_ownership(data)

def patch_transfer_ownership(data):
    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if user is the owner of the store
        store_name = data['store_name']
        if cu.check_if_user_is_owner(username, store_name):

            new_owner = data['new_owner']

            # check if new owner exists
            if cu.check_if_username_exists(new_owner):

                # check if new owner is a proprietor
                if cu.check_if_user_is_proprietor(new_owner):

                    # check if store exists
                    if cu.check_if_store_exists(store_name):

                        # check password
                        password = data['password']
                        new_owner_password = data['new_owner_password']

                        # check new owner password
                        if cu.check_is_user(new_owner, new_owner_password):

                            # check user password
                            if cu.check_is_user(username, password):

                                # finally
                                dynamodb = cu.bt3.resource("dynamodb")
                                Store_Table = dynamodb.Table('PRO305_Store_Table')

                                # updating store in Store_Table
                                Store_Table.update_item(
                                    Key={'store_name': store_name},
                                    UpdateExpression="SET proprietor = :i",
                                    ExpressionAttributeValues={
                                        ':i': new_owner
                                    }
                                )

                                # updating store in Proprietor_Table
                                Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
                                Proprietor_Table.update_item(
                                    Key={'username': username, 'password': password},
                                    UpdateExpression="REMOVE properties[0]",
                                    ConditionExpression="contains(properties, :i)",
                                    ExpressionAttributeValues={
                                        ':i': store_name
                                    }
                                )
                                Proprietor_Table.update_item(
                                    Key={'username': new_owner, 'password': new_owner_password},
                                    UpdateExpression="SET properties = list_append(properties, :i)",
                                    ExpressionAttributeValues={
                                        ':i': [store_name]
                                    }
                                )

                                # generating response
                                body = {"message": "Store ownership transferred", "store_name": store_name}
                                return cu.create_response(200, body)

                            else:
                                # generating response
                                return cu.create_response(400, "Invalid username or password")

                        else:
                            # generating response
                            return cu.create_response(400, "Invalid new owner username or password")

                    else:
                        # generating response
                        return cu.create_response(400, "Store does not exist")

                else:
                    # generating response
                    return cu.create_response(400, "New owner is not a proprietor")
            else:
                # generating response
                return cu.create_response(400, "New owner does not exist")
        else:
            # generating response
            return cu.create_response(400, "User is not the owner of the store")
    else:
        # generating response
        return cu.create_response(400, "User does not exist")