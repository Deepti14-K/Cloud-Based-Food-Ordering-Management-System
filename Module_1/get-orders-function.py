import json
import boto3 
import random
from boto3.dynamodb.conditions import Key, Attr

# DynamoDB table client
dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'orders-table'

def lambda_handler(event, context):
    
    """ The function reads the DynamoDB table and returns all the orders for the user 
    with the user_id passed to the route /get-order/{id} """
    
    try:
        user_id = event['rawPath'].split("/")[-1]
        table = dynamodb_client.Table(dynamodb_table_name)
        
        # query the global secondary index user_id-index
        response = table.query(
                    IndexName='user_id-index',
                    KeyConditionExpression=Key('user_id').eq(user_id)
                    )
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'status_code': 200,
                'body': response['Items']
            }
            
        return {
            'status_code': 400,
            'body': "Unable to get orders, verify the DynamoDB table configuration"
        }
            
    except Exception as e:
        return {
            'status_code': 500,
            'body': "Unable to get orders due to an internal server error" 
        }
