import boto3 as bt3


dynamodb = bt3.resource('dynamodb')
Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")


def lambda_handler(event, context):
    # authorizer
    authorizationToken = event['authorizationToken']
    print("authorizationToken: ", authorizationToken)


    return validateUser(authorizationToken)


def generatePolicy(principalId, effect, resource):
    authResponse = {'principalId': principalId, 'policyDocument': {'Version': '2012-10-17', 'Statement': [
        {'Action': 'execute-api:Invoke', 'Effect': effect, 'Resource': resource}]}}

    return authResponse


def validateUser(username):
    try:
        print("Checking username in user table")
        response = Registered_User_Table.get_item(Key={"username": username})
        print("response: ", response)

        if "Item" in response:
            print("User Found")
            return generatePolicy(username, 'Allow', "arn:aws:execute-api:us-west-2:408386168496:2nrymwm4bd/*/*/users")

        else:
            print("User not Found")
            return generatePolicy('', 'Deny', "")

    except Exception as e:
        print("ERROR: ", e)
        return generatePolicy('', 'Deny', "")