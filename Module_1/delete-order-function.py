import json
import boto3 
import random
import base64
from boto3.dynamodb.conditions import Key, Attr

dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'orders-table'

def lambda_handler(event, context):
    
    """ The function deletes an order placed from the orders-table. 
    The order can be deleted only by the user who placed the order  """
    
    try:
        table = dynamodb_client.Table(dynamodb_table_name)
        order = json.loads(base64.b64decode(event['body']).decode("utf-8"))
        order_id, user_id = order['order_id'], order['user_id']
        response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('order_id').eq(order_id))
    
        """ Only if there is a single order with that index and the user_id 
        matches the user_id passed, delete the order """
        
        if len(response['Items']) == 1 and response['Items'][0]['user_id'] == user_id:
            response = table.delete_item(
                Key={
                    'order_id': order_id
                }
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'status_code': 200,
                    'body': "Order deleted successfully"
                }
        
        return {
            'status_code': 400,
            'body': "Unable to delete order, verify the order_id and user_id"
        }
        
    except Exception as e:
        return {
            'status_code': 500,
            'body':"Unable to delete order due to an internal server error"
        }
