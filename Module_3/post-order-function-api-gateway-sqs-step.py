import json
import boto3 
import random
import string
import base64 
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid

dynamodb_client = boto3.resource('dynamodb')
step_client = boto3.client('stepfunctions')
dynamodb_table_name = 'orders-table'

def generate_random_order_id():
    order_id = ''.join(random.choice(string.digits) for i in range(9))
    return order_id

def get_current_date_and_time():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M")
    return formatted_datetime


def lambda_handler(event, context):
    try:
        success_adding_all_messages = True
        table = dynamodb_client.Table(dynamodb_table_name)
        
        for record in event['Records']:
            order = json.loads(record['body'])
            order_id = generate_random_order_id()
            # order status written as PENDING, and step function invoked
            data = {
                    "order_id": order_id,
                    "user_id" : order["user_id"],
                    "restaurant_id": order['restaurant_id'],
                    "order_date": get_current_date_and_time(),
                    "item_name": order["item_name"],
                    "order_status": "PENDING"
                }
            response = table.put_item(Item=data)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                success_adding_all_messages = False
            else:
                # invoke step function only if addition to Dynamo DB is successful
                input = {'order_id': order_id}
                execution_id = str(uuid.uuid1())
                response = step_client.start_execution(
                    stateMachineArn='your-state-machine-arn',
                    name=execution_id,
                    input=json.dumps(input))
             
        if success_adding_all_messages:
            return {
                'status_code': 200,
                'body': "Order placed successfully"
            }
        
        return {
            'status_code': 400,
            'body': "Unable to place order, verify the order details"
        }
        
    except Exception as e:
        return {
            'status_code': 500,
            'body':"Unable to place order due to an internal server error"
        }