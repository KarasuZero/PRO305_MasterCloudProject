import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "POST_Get_Cart":
        return post_get_cart(data)

    elif operation == "POST_Checkout":
        return post_checkout(data)

def post_get_cart(data):
    username = data['username']
    password = data['password']

    # dynamoDB stuff
    DynamoDB = cu.bt3.resource("dynamodb")
    User_Table = DynamoDB.Table("PRO305_User_Table")

    # check if user exists
    if cu.check_if_username_exists(username):

        # check password
        if cu.check_is_user(username, password):
            # get item
            response = User_Table.get_item(Key={'username': username, 'password': password})
            item = response['Item']

            # generate response
            return cu.create_response(200, item['Cart'])

        else:
            # generate response
            return cu.create_response(400, "Password is incorrect")

    else:
        # generate response
        return cu.create_response(400, "User does not exist")

def post_checkout(data):
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

            # grab email
            email = item['email']

            # grab name
            name = item['name']

            # send cart to sqs
            cu.send_cart(username, password, email, name)

            # generate response
            return cu.create_response(200, "Order placed")


        else:
            # generate response
            return cu.create_response(400, "Password is incorrect")

    else:
        # generate response
        return cu.create_response(400, "User does not exist")