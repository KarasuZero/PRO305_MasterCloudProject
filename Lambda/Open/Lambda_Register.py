import custom_util as cu


def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])

    loaded_body = cu.json.load(decoded_body)

    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "POST_Register_User":
        return post_register_user(data)


def post_register_user(data):
    username = data['username']
    password = data['password']

    # DynamoDB stuff
    dynamodb = cu.bt3.resource('dynamodb')
    Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")
    User_Table = dynamodb.Table("PRO305_User_Table")
