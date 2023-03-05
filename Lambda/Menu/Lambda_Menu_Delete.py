import custom_util as cu

def lambda_handler(event, context):
    # grab body and do b64 stuff
    decoded_body = cu.b64Decode(event['body'])
    loaded_body = cu.json.loads(decoded_body)

    # grabbing op and data
    operation = loaded_body['operation']
    data = loaded_body['data']

    if operation == "DELETE_Delete_Menu":  # works
        return delete_menu(data)

def delete_menu(data):
    dynamodb = cu.bt3.resource("dynamodb")
    Menu_Table = dynamodb.Table('PRO305_Menu_Table')

    # grabbing data
    id = data['menu_id']

    # delete menu
    Menu_Table.delete_item(Key={'menu_id': id})

    body = {"message": "Menu Deleted"}

    return cu.create_response(200, cu.json.dumps(body))
