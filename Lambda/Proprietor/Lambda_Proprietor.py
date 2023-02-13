import custom_util as cu

def lambda_handler(event, context):

    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    # passing data to the correct method base on op
    if operation == "POST_Create_Store":
        return POST_Create_Store(data)

    elif operation == "DELETE_Delete_Store":
        return DELETE_Delete_Store(data)

    elif operation == "PATCH_Transfer_Ownership":
        return PATCH_Transfer_Ownership(data)


def POST_Create_Store(data):

    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if user is proprietor
        if cu.check_if_user_is_proprietor(username):

            password = data['password']

            # validate user
            if cu.check_is_user(username,password):

                # check if store exists
                store_name = data['storename']

                if cu.check_if_store_exists(store_name):

                    # generating response
                    return cu.create_response(400, "Store already exists")

                else:

                    # all checks passed
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    des = data['description']
                    loc = data['location']
                    city = data['city']
                    state = data['state']
                    zip = data['zip']
                    phone = data['phone']
                    email = data['email']
                    website = data['website']
                    hours = data['hours']

                    # inserting into Store_Table
                    Store_Table.put_item(Item={
                        "storename": store_name,
                        "description": des,
                        "location": loc,
                        "city": city,
                        "state": state,
                        "zip": zip,
                        "phone": phone,
                        "email": email,
                        "website": website,
                        "hours": hours,
                        "menu": [],
                        "proprietor": username
                    })

                    # inserting into Proprietor_Table
                    Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
                    Proprietor_Table.update_item(
                        Key={'username': username,'password': password},
                        UpdateExpression="SET properties = list_append(properties, :i)",
                        ExpressionAttributeValues={
                            ':i': [store_name]
                        }
                    )

                    # generating response
                    body = {"message": "Store Created", "storename": store_name}
                    return cu.create_response(200, body)

            else:
                # generating response
                return cu.create_response(400, "Invalid username or password")

        else:
            # generating response
            return cu.create_response(400, "User is not a proprietor")

    else:
        # generating response
        return cu.create_response(400, "User does not exist")

def DELETE_Delete_Store(data):
    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if store exists
        store_name = data['storename']
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
                    Store_Table.delete_item(Key={'storename': store_name})

                    # deleting store from Proprietor_Table
                    Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
                    Proprietor_Table.update_item(
                        Key={'username': username,'password': password},
                        UpdateExpression="REMOVE properties[0]",
                        ConditionExpression="contains(properties, :i)",
                        ExpressionAttributeValues={
                            ':i': store_name
                        }
                    )

                    # generating response
                    body = {"message": "Store Deleted", "storename": store_name}
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

def PATCH_Transfer_Ownership(data):

    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if user is the owner of the store
        store_name = data['storename']
        if cu.check_if_user_is_owner(username, store_name):

            new_owner = data['newowner']

            # check if new owner exists
            if cu.check_if_username_exists(new_owner):

                # check if new owner is a proprietor
                if cu.check_if_user_is_proprietor(new_owner):

                    # check if store exists
                    if cu.check_if_store_exists(store_name):

                        # check password
                        password = data['password']
                        new_owner_password = data['newownerpassword']

                        # check new owner password
                        if cu.check_is_user(new_owner, new_owner_password):

                            # check user password
                            if cu.check_is_user(username, password):

                                # finally
                                dynamodb = cu.bt3.resource("dynamodb")
                                Store_Table = dynamodb.Table('PRO305_Store_Table')

                                # updating store in Store_Table
                                Store_Table.update_item(
                                    Key={'storename': store_name},
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
                                body = {"message": "Store ownership transfered", "storename": store_name}
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


