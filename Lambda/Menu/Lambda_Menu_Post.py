import custom_util as cu
from uuid import uuid4

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "POST_Create_Menu":  # works
        return post_create_menu(data)


def post_create_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = str(uuid4())
    data['menu_id'] = id
    items = data['items']

    # for each item in items array add item_id
    for item in items:
        item_id = str(uuid4())
        item['item_id'] = item_id
    # insert into Menu_Table
    Menu_Table.put_item(Item=data)

    body = {"message": "Menu Created", "data": data}

    return cu.create_response(200, cu.json.dumps(body))