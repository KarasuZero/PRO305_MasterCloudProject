import custom_util as cu


def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    # passing data to the correct method base on op
    if operation == "PATCH_Add_Menu":
        return patch_add_menu(data)

    elif operation == "PATCH_Remove_Menu":
        return patch_remove_menu(data)

    elif operation == "PATCH_Edit_Location":
        return patch_edit_loc(data)

    elif operation == "PATCH_Edit_Hours":
        return patch_edit_hours(data)

    elif operation == "PATCH_Edit_Description":
        return patch_edit_des(data)

    elif operation == "PATCH_Edit_Address":
        return patch_edit_address(data)

    elif operation == "PATCH_Edit_Contact":
        return patch_edit_contact(data)

    elif operation == "PATCH_Edit_Email":
        return patch_edit_email(data)

    elif operation == "PATCH_Edit_Website":
        return patch_edit_website(data)


def patch_add_menu(data):
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

                    # check if menu exists
                    menu_id = data['menu_id']

                    if cu.check_if_menu_exists(menu_id):

                        # check if menu is already in store
                        if cu.check_if_menu_in_store(menu_id, store_name):
                            # generating response
                            return cu.create_response(400, "Menu already in store")

                        else:

                            # insert into dynamodb
                            dynamodb = cu.bt3.resource("dynamodb")
                            Store_Table = dynamodb.Table('PRO305_Store_Table')

                            # update store
                            Store_Table.update_item(
                                Key={'store_name': store_name},
                                UpdateExpression="SET menu_list = list_append(menu_list, :menu_id)",
                                ExpressionAttributeValues={
                                    ':menu_id': [menu_id]
                                }
                            )

                            # generating response
                            return cu.create_response(200, "Menu added to store")

                    else:
                        # generating response
                        return cu.create_response(400, "Menu does not exist")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")

def patch_remove_menu(data):
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

                    # check if menu exists
                    menu_id = data['menu_id']

                    if cu.check_if_menu_exists(menu_id):

                        # check if menu is in store
                        if cu.check_if_menu_in_store(menu_id, store_name):
                            # remove menu from store
                            dynamodb = cu.bt3.resource("dynamodb")
                            Store_Table = dynamodb.Table('PRO305_Store_Table')

                            # update store
                            Store_Table.update_item(
                                Key={'store_name': store_name},
                                UpdateExpression="REMOVE menu_list[0]",
                                ConditionExpression="menu_list[0] = :menu_id",
                                ExpressionAttributeValues={
                                    ':menu_id': menu_id
                                }
                            )

                            # generating response
                            return cu.create_response(200, "Menu removed from store")

                        else:
                            # generating response
                            return cu.create_response(400, "Menu is not in store")

                    else:
                        # generating response
                        return cu.create_response(400, "Menu does not exist")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")

def patch_edit_loc(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_loc = data['new_loc']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set loc = :l",
                        ExpressionAttributeValues={
                            ':l': new_loc
                        }
                    )

                    return cu.create_response(200, "Store location updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_hours(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_hours = data['new_hours']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set hours = :h",
                        ExpressionAttributeValues={
                            ':h': new_hours
                        }
                    )

                    return cu.create_response(200, "Store hours updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_des(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_des = data['new_des']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set description = :D",
                        ExpressionAttributeValues={
                            ':D': new_des
                        }
                    )

                    return cu.create_response(200, "Store description updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_address(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_city = data['new_city']
                    new_state = data['new_state']
                    new_zip = data['new_zip']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set city = :c, st = :s, zipcode = :z",
                        ExpressionAttributeValues={
                            ':c': new_city,
                            ':s': new_state,
                            ':z': new_zip
                        }
                    )

                    return cu.create_response(200, "Store address updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_contact(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_phone = data['new_phone']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set phone = :p",
                        ExpressionAttributeValues={
                            ':p': new_phone
                        }
                    )

                    return cu.create_response(200, "Store contact updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_email(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_email = data['new_email']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set email = :e",
                        ExpressionAttributeValues={
                            ':e': new_email
                        }
                    )

                    return cu.create_response(200, "Store email updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")


def patch_edit_website(data):
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

                    # insert into dynamodb
                    dynamodb = cu.bt3.resource("dynamodb")
                    Store_Table = dynamodb.Table('PRO305_Store_Table')

                    # grabbing attributes
                    new_website = data['new_website']

                    # updating store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="set website = :w",
                        ExpressionAttributeValues={
                            ':w': new_website
                        }
                    )

                    return cu.create_response(200, "Store website updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not the owner of the store")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")
    else:
        # generating response
        return cu.create_response(400, "Username does not exist")
