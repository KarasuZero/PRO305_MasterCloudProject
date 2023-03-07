import boto3 as bt3

dynamodb = bt3.resource('dynamodb')
Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")


def lambda_handler(event, context):
    # authorizer
    authorizationToken = event['authorizationToken']
    print("authorizationToken: ", authorizationToken)

    return validateUser(event)


def generatePolicy(principalId, effect, resource):
    authResponse = {'principalId': principalId, 'policyDocument': {'Version': '2012-10-17', 'Statement': [
        {'Action': 'execute-api:Invoke', 'Effect': effect, 'Resource': resource}]}}

    return authResponse


def validateUser(event):
    try:
        username = event['authorizationToken']
        print("Checking username in user table")
        response = Registered_User_Table.get_item(Key={"username": username})
        print("response: ", response)

        if "Item" in response:
            print("User Found")

            # Check if user is a proprietor
            if response["Item"]["role"] == "PROPRIETOR":
                print("User is a proprietor")
                return generatePolicy(username, 'Allow', event['methodArn'])

            else:
                print("User is not a Proprietor")
                return generatePolicy('', 'Deny', "")

        else:
            print("User not Found")
            return generatePolicy('', 'Deny', "")

    except Exception as e:
        print("ERROR: ", e)
        return generatePolicy('', 'Deny', "")