import custom_util as cu


def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    # passing data to the correct method base on op
    if operation == "POST_Register_User":
        return post_register_user(data)
    elif operation == "POST_Register_Proprietor":
        return post_register_proprietor(data)



def post_register_user(data):
    username = data['username']
    email = data['email']
    # TODO verify email format

    # check if username exists
    exist = cu.check_if_username_exists(username)

    if exist:
        # generating response
        return cu.create_response(400, "Username already exists")

    else:
        # dynamodb stuff
        dynamodb = cu.bt3.resource("dynamodb")
        Registered_User_Table = dynamodb.Table('PRO305_Registered_User_Table')
        User_Table = dynamodb.Table('PRO305_User_Table')

        # grabbing password and name
        password = data['password']
        name = data['name']

        # inserting into Registered_User_Table
        Registered_User_Table.put_item(Item={
            "username": username,
            "role": "USER"})

        # inserting into User_Table
        User_Table.put_item(Item={
            "username": username,
            "password": password,
            "name": name,
            "email": email,
            "Cart": []
        })

        # generating response
        body = {"message": "User Created", "username": username, "password": password, "name": name}
        # TODO send email content to message queue? and then let the email service handle it?

        return cu.create_response(200, cu.json.dumps(body))

def post_register_proprietor(data):
    username = data['username']
    email = data['email']
    # TODO verify email format

    # check if username exists
    if cu.check_if_username_exists(username):
        # generating response
        return cu.create_response(400, "Username already exists")

    else:
        # dynamodb stuff
        dynamodb = cu.bt3.resource("dynamodb")
        Registered_User_Table = dynamodb.Table('PRO305_Registered_User_Table')
        Proprietor_Table = dynamodb.Table('PRO305_Proprietor_Table')
        User_Table = dynamodb.Table('PRO305_User_Table')

        # grabbing password name and phone number
        password = data['password']
        name = data['name']
        phone = data['phone']

        # inserting into Registered_User_Table
        Registered_User_Table.put_item(Item={
            "username": username,
            "role": "PROPRIETOR"})

        # inserting into Proprietor_Table
        Proprietor_Table.put_item(Item={
            "username": username,
            "password": password,
            "name": name,
            "email": email,
            "phone": phone,
            "properties": []
        })

        # inserting into User_Table
        User_Table.put_item(Item={
            "username": username,
            "password": password,
            "name": name,
            "email": email,
            "Cart": []
        })

        # generating response
        body = {"message": "Proprietor Created", "username": username, "password": password, "name": name, "phone": phone}
        # TODO send email content to message queue? and then let the email service handle it?

        return cu.create_response(200, cu.json.dumps(body))