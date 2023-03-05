import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "POST_Create_Store":
        return post_create_store(data)


def post_create_store(data):
    username = data['username']

    # check if username exists
    if cu.check_if_username_exists(username):

        # check if user is proprietor
        if cu.check_if_user_is_proprietor(username):

            password = data['password']

            # validate user
            if cu.check_is_user(username, password):

                # check if store exists
                store_name = data['store_name']

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
                    zipcode = data['zipcode']
                    phone = data['phone']
                    email = data['email']
                    website = data['website']
                    hours = data['hours']

                    # inserting into Store_Table
                    Store_Table.put_item(Item={
                        "store_name": store_name,
                        "description": des,
                        "loc": loc,
                        "city": city,
                        "st": state,
                        "zipcode": zipcode,
                        "phone": phone,
                        "email": email,
                        "website": website,
                        "hours": hours,
                        "menu_list": [],
                        "proprietor": username
                    })

                    # inserting into Proprietor_Table
                    Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
                    Proprietor_Table.update_item(
                        Key={'username': username, 'password': password},
                        UpdateExpression="SET properties = list_append(properties, :i)",
                        ExpressionAttributeValues={
                            ':i': [store_name]
                        }
                    )

                    # generating response
                    body = {"message": "Store Created", "store_name": store_name}
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