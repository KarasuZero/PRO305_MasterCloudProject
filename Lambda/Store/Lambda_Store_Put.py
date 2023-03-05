import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "PUT_Update_Store":
        return put_update_store(data)


def put_update_store(data):
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

                    # grabbing attributes from data
                    store_name = data['store_name']
                    store_location = data['loc']
                    store_hours = data['hours']
                    store_description = data['desc']
                    store_state = data['st']
                    store_city = data['city']
                    store_zipcode = data['zipcode']
                    store_contact = data['phone']
                    store_email = data['email']
                    store_website = data['website']
                    store_menu = data['menu_list']


                    # dynamodb stuff
                    dynamodb = cu.bt3.resource('dynamodb')
                    Store_Table = dynamodb.Table("PRO305_Store_Table")

                    # update store
                    Store_Table.update_item(
                        Key={'store_name': store_name},
                        UpdateExpression="SET loc = :store_location, hours = :store_hours, "
                                         "description = :store_description, st = :store_state, "
                                         "city = :store_city, zipcode = :store_zipcode, "
                                         "phone = :store_contact, email = :store_email, "
                                         "website = :store_website, menu_list = :store_menu",

                        ExpressionAttributeValues={
                            ':store_location': store_location,
                            ':store_hours': store_hours,
                            ':store_description': store_description,
                            ':store_contact': store_contact,
                            ':store_email': store_email,
                            ':store_website': store_website,
                            ':store_menu': store_menu,
                            ':store_state': store_state,
                            ':store_city': store_city,
                            ':store_zipcode': store_zipcode
                        }
                    )

                    # generating response
                    return cu.create_response(200, "Store updated")

                else:
                    # generating response
                    return cu.create_response(400, "Password is incorrect")

            else:
                # generating response
                return cu.create_response(400, "User is not owner")

        else:
            # generating response
            return cu.create_response(400, "Store does not exist")

    else:
        # generating response
        return cu.create_response(400, "Username does not exist")
