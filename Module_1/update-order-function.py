import json
import boto3 
import random
import base64
from boto3.dynamodb.conditions import Key, Attr

dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'orders-table'

def lambda_handler(event, context):
    
    """ The function updates the details of an existing order. 
    Either the item_name or restaurant_id or both fields can be updated  """
     
    try:

        table = dynamodb_client.Table(dynamodb_table_name)
        order = json.loads(base64.b64decode(event['body']).decode("utf-8"))
        order_id, user_id = order['order_id'], order['user_id']
        response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('order_id').eq(order_id))
        if len(response['Items']) == 1 and response['Items'][0]['user_id'] == user_id:
            response = table.update_item(
                Key={'order_id': order_id},
                UpdateExpression="set item_name=:n, restaurant_id=:r",
                ExpressionAttributeValues={
                    ':n': order.get("item_name", response['Items'][0]["item_name"]),
                    ':r': order.get("restaurant_id", response['Items'][0]["restaurant_id"])
                },
                ReturnValues="UPDATED_NEW")
            
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'status_code': 200,
                    'body': "Order updated successfully"
                }
        
        return {
            'status_code': 400,
            'body': "Unable to update order, verify the order_id and user_id"
        }
        
    except Exception as e:
        return {
            'status_code': 500,
            'body':"Unable to update order due to an internal server error"
        }
