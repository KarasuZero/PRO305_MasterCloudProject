# import boto3 as bt3
#
# # import base64 as b64
#
# dynamodb = bt3.resource('dynamodb')
# Registered_User_Table = dynamodb.Table("PRO305_Registered_User_Table")
#
#
# def lambda_handler(event, context):
#     # authorizer
#     authorizationToken = event['authToken']
#     print("authorizationToken: ", authorizationToken)
#
#     # decoded = b64Decode(authorizationToken)
#     # print(decoded)
#
#     return validateUser(authorizationToken)
#
#
# # def b64Decode(body_element):
# #     return b64.b64decode(body_element).decode('utf-8')
#
# def generatePolicy(principalId, effect, resource):
#     authResponse = {'principalId': principalId, 'policyDocument': {'Version': '2012-10-17', 'Statement': [
#         {'Action': 'execute-api:Invoke', 'Effect': effect, 'Resource': resource}]}}
#
#     return authResponse
#
#
# def validateUser(username):
#     try:
#         print("Checking username in user table")
#         response = Registered_User_Table.get_item(Key={"username": username})
#         print("response: ", response)
#
#         if "Item" in response:
#             print("User Found")
#             return generatePolicy(username, 'Allow', "arn:aws:execute-api:us-west-2:408386168496:bt594c8e2e/*/*/user")
#
#         else:
#             print("User not Found")
#             return generatePolicy('', 'Deny', "")
#
#     except Exception as e:
#         print("ERROR: ", e)
#         return generatePolicy('', 'Deny', "")