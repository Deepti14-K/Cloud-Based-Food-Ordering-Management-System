import json
import boto3 
import random
import string
import base64 
from boto3.dynamodb.conditions import Key, Attr
import datetime

dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'orders-table'


def generate_random_order_id():
    # generate a random order id comprising digits 0-9 (length is 9)
    order_id = ''.join(random.choice(string.digits) for i in range(9))
    return order_id

def get_current_date_and_time():
    # Return the current date and time in UTC
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M")
    return formatted_datetime


def lambda_handler(event, context):
    """ The function adds an order placed by the user 
    to the orders-table. The order_id is randomly generated; 
    order_status is successful; time of placing the order in UTC in recorded """

    try:
        table = dynamodb_client.Table(dynamodb_table_name)
        order = base64.b64decode(event['body']).decode("utf-8")
        order = json.loads(order)
        order_id = generate_random_order_id()
        data = {
                "order_id": order_id,
                "user_id" : order["user_id"],
                "restaurant_id": order['restaurant_id'],
                "order_date": get_current_date_and_time(),
                "item_name": order["item_name"],
                "order_status": "SUCCESS"
            }
        response = table.put_item(Item=data)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'status_code': 200,
                'body' : "Order successfully added, order_id is {}".format(order_id)
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